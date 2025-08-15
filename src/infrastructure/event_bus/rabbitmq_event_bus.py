"""RabbitMQ-based distributed event bus implementation."""

import asyncio
import json
import logging
from typing import Any, Callable, Dict, List, Optional
from dataclasses import asdict

import aio_pika
from aio_pika import connect_robust, Message, DeliveryMode
from aio_pika.patterns import RPC

from domain.event import KnowledgeEvent
from application.event_bus import EventBus


logger = logging.getLogger(__name__)


class RabbitMQEventBus(EventBus):
    """
    Distributed event bus using RabbitMQ.
    
    This implementation provides:
    - Reliable message delivery with acknowledgments
    - Support for multiple consumers
    - Dead letter queue for failed messages
    - RPC pattern for request-response
    - Automatic reconnection on failures
    """

    def __init__(
        self,
        connection_url: str = "amqp://guest:guest@localhost/",
        exchange_name: str = "knowledge_events",
        queue_prefix: str = "kg_",
        max_retries: int = 3,
        retry_delay: float = 1.0,
    ):
        self.connection_url = connection_url
        self.exchange_name = exchange_name
        self.queue_prefix = queue_prefix
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        
        # Connection and channel management
        self.connection: Optional[aio_pika.Connection] = None
        self.channel: Optional[aio_pika.Channel] = None
        self.exchange: Optional[aio_pika.Exchange] = None
        
        # Local handlers for backward compatibility
        self._local_handlers: Dict[str, List[Callable]] = {}
        
        # RPC support
        self.rpc: Optional[RPC] = None
        
        # Consumer tasks
        self._consumer_tasks: List[asyncio.Task] = []
        self._is_connected = False

    async def connect(self) -> None:
        """Establish connection to RabbitMQ."""
        try:
            logger.info(f"Connecting to RabbitMQ at {self.connection_url}")
            
            # Connect to RabbitMQ
            self.connection = await connect_robust(self.connection_url)
            self.channel = await self.connection.channel()
            
            # Set QoS for better performance
            await self.channel.set_qos(prefetch_count=10)
            
            # Declare exchange
            self.exchange = await self.channel.declare_exchange(
                self.exchange_name,
                aio_pika.ExchangeType.TOPIC,
                durable=True
            )
            
            # Initialize RPC
            self.rpc = await RPC.create(self.channel)
            
            self._is_connected = True
            logger.info("Successfully connected to RabbitMQ")
            
        except Exception as e:
            logger.error(f"Failed to connect to RabbitMQ: {e}")
            self._is_connected = False
            raise

    async def disconnect(self) -> None:
        """Close connection to RabbitMQ."""
        try:
            # Cancel all consumer tasks
            for task in self._consumer_tasks:
                if not task.done():
                    task.cancel()
                    try:
                        await task
                    except asyncio.CancelledError:
                        pass
            
            # Close channel and connection
            if self.channel:
                await self.channel.close()
            if self.connection:
                await self.connection.close()
                
            self._is_connected = False
            logger.info("Disconnected from RabbitMQ")
            
        except Exception as e:
            logger.error(f"Error disconnecting from RabbitMQ: {e}")

    async def publish(self, event: KnowledgeEvent, routing_key: Optional[str] = None) -> None:
        """Publish a knowledge event to the distributed event bus."""
        if not self._is_connected:
            logger.warning("Not connected to RabbitMQ, falling back to local handlers")
            await self._publish_local(event)
            return
        
        try:
            # Convert event to JSON
            event_data = asdict(event)
            message_body = json.dumps(event_data, default=str).encode()
            
            # Create message with persistent delivery
            message = Message(
                body=message_body,
                delivery_mode=DeliveryMode.PERSISTENT,
                content_type="application/json",
                headers={
                    "event_type": event.action,
                    "role": event.role.value,
                    "timestamp": str(event.timestamp) if hasattr(event, 'timestamp') else None
                }
            )
            
            # Determine routing key
            if routing_key is None:
                routing_key = event.action
            
            # Publish to exchange
            await self.exchange.publish(message, routing_key=routing_key)
            
            logger.debug(f"Published event {event.action} with routing key {routing_key}")
            
        except Exception as e:
            logger.error(f"Failed to publish event {event.action}: {e}")
            # Fallback to local handlers
            await self._publish_local(event)

    async def subscribe(self, event_type: str, handler: Callable) -> None:
        """Subscribe to events of a specific type."""
        # Register local handler for backward compatibility
        if event_type not in self._local_handlers:
            self._local_handlers[event_type] = []
        self._local_handlers[event_type].append(handler)
        
        # Also subscribe to RabbitMQ if connected
        if self._is_connected:
            await self._subscribe_rabbitmq(event_type, handler)

    async def _subscribe_rabbitmq(self, event_type: str, handler: Callable) -> None:
        """Subscribe to RabbitMQ queue for specific event type."""
        try:
            # Create queue for this event type
            queue_name = f"{self.queue_prefix}{event_type}"
            queue = await self.channel.declare_queue(
                queue_name,
                durable=True,
                arguments={
                    "x-dead-letter-exchange": f"{self.exchange_name}_dlx",
                    "x-dead-letter-routing-key": event_type
                }
            )
            
            # Bind queue to exchange with routing key
            await queue.bind(self.exchange, event_type)
            
            # Start consuming messages
            consumer_task = asyncio.create_task(
                self._consume_messages(queue, handler, event_type)
            )
            self._consumer_tasks.append(consumer_task)
            
            logger.info(f"Subscribed to RabbitMQ queue {queue_name} for event type {event_type}")
            
        except Exception as e:
            logger.error(f"Failed to subscribe to RabbitMQ for {event_type}: {e}")

    async def _consume_messages(self, queue: aio_pika.Queue, handler: Callable, event_type: str) -> None:
        """Consume messages from a queue."""
        try:
            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    async with message.process():
                        try:
                            # Parse event from message
                            event_data = json.loads(message.body.decode())
                            event = KnowledgeEvent(**event_data)
                            
                            # Call handler
                            if asyncio.iscoroutinefunction(handler):
                                await handler(event)
                            else:
                                handler(event)
                                
                            logger.debug(f"Processed event {event.action} from queue {queue.name}")
                            
                        except Exception as e:
                            logger.error(f"Error processing message from queue {queue.name}: {e}")
                            # Message will be rejected and sent to dead letter queue
                            await message.reject(requeue=False)
                            
        except Exception as e:
            logger.error(f"Error consuming from queue {queue.name}: {e}")

    async def _publish_local(self, event: KnowledgeEvent) -> None:
        """Publish event to local handlers (fallback)."""
        handlers = self._local_handlers.get(event.action, [])
        for handler in handlers:
            try:
                if asyncio.iscoroutinefunction(handler):
                    await handler(event)
                else:
                    handler(event)
            except Exception as e:
                logger.error(f"Error in local handler for {event.action}: {e}")

    async def publish_batch(self, events: List[KnowledgeEvent], routing_key: Optional[str] = None) -> None:
        """Publish multiple events in a batch."""
        if not self._is_connected:
            logger.warning("Not connected to RabbitMQ, falling back to local handlers")
            for event in events:
                await self._publish_local(event)
            return
        
        try:
            # Use transaction for batch publishing
            async with self.channel.transaction():
                for event in events:
                    await self.publish(event, routing_key)
                    
            logger.info(f"Published batch of {len(events)} events")
            
        except Exception as e:
            logger.error(f"Failed to publish batch: {e}")
            # Fallback to local handlers
            for event in events:
                await self._publish_local(event)

    async def call_rpc(self, method: str, payload: Dict[str, Any], timeout: float = 30.0) -> Dict[str, Any]:
        """Make an RPC call using RabbitMQ."""
        if not self._is_connected or not self.rpc:
            raise RuntimeError("Not connected to RabbitMQ or RPC not available")
        
        try:
            # Convert payload to JSON
            message_body = json.dumps(payload).encode()
            
            # Make RPC call
            response = await asyncio.wait_for(
                self.rpc.call(method, message_body),
                timeout=timeout
            )
            
            # Parse response
            return json.loads(response.body.decode())
            
        except asyncio.TimeoutError:
            raise TimeoutError(f"RPC call to {method} timed out after {timeout}s")
        except Exception as e:
            logger.error(f"RPC call to {method} failed: {e}")
            raise

    async def register_rpc_handler(self, method: str, handler: Callable) -> None:
        """Register an RPC handler for a specific method."""
        if not self._is_connected or not self.rpc:
            raise RuntimeError("Not connected to RabbitMQ or RPC not available")
        
        try:
            async def rpc_handler(message):
                try:
                    # Parse request
                    request_data = json.loads(message.body.decode())
                    
                    # Call handler
                    if asyncio.iscoroutinefunction(handler):
                        result = await handler(request_data)
                    else:
                        result = handler(request_data)
                    
                    # Return response
                    response_body = json.dumps(result).encode()
                    return response_body
                    
                except Exception as e:
                    logger.error(f"Error in RPC handler for {method}: {e}")
                    # Return error response
                    error_response = {"error": str(e)}
                    return json.dumps(error_response).encode()
            
            # Register handler
            await self.rpc.register(method, rpc_handler)
            logger.info(f"Registered RPC handler for method {method}")
            
        except Exception as e:
            logger.error(f"Failed to register RPC handler for {method}: {e}")
            raise

    @property
    def is_connected(self) -> bool:
        """Check if connected to RabbitMQ."""
        return self._is_connected

    async def health_check(self) -> Dict[str, Any]:
        """Perform health check of the RabbitMQ connection."""
        try:
            if not self._is_connected:
                return {"status": "disconnected", "error": "Not connected to RabbitMQ"}
            
            # Check connection and channel
            if not self.connection.is_closed and not self.channel.is_closed:
                return {
                    "status": "healthy",
                    "connection": "connected",
                    "channel": "open",
                    "exchange": self.exchange_name
                }
            else:
                return {"status": "unhealthy", "error": "Connection or channel closed"}
                
        except Exception as e:
            return {"status": "error", "error": str(e)}

    async def get_queue_info(self, event_type: str) -> Dict[str, Any]:
        """Get information about a specific queue."""
        if not self._is_connected:
            return {"error": "Not connected to RabbitMQ"}
        
        try:
            queue_name = f"{self.queue_prefix}{event_type}"
            queue = await self.channel.declare_queue(queue_name, passive=True)
            
            return {
                "queue_name": queue_name,
                "event_type": event_type,
                "message_count": queue.declaration_result.message_count,
                "consumer_count": queue.declaration_result.consumer_count
            }
            
        except Exception as e:
            return {"error": f"Failed to get queue info: {e}"}
