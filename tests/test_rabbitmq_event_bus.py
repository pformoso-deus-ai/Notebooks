"""Tests for the RabbitMQ event bus implementation."""

import asyncio
import json
import unittest
from unittest.mock import Mock, patch, AsyncMock
import os
import sys

# Ensure the src directory is on the import path
_TEST_DIR = os.path.dirname(__file__)
_SRC_PATH = os.path.abspath(os.path.join(_TEST_DIR, "..", "src"))
if _SRC_PATH not in sys.path:
    sys.path.insert(0, _SRC_PATH)

from infrastructure.event_bus.rabbitmq_event_bus import RabbitMQEventBus
from domain.event import KnowledgeEvent
from domain.roles import Role


class TestRabbitMQEventBus(unittest.IsolatedAsyncioTestCase):
    """Test cases for the RabbitMQ Event Bus."""

    async def asyncSetUp(self):
        """Set up test fixtures."""
        self.event_bus = RabbitMQEventBus(
            connection_url="amqp://guest:guest@localhost/",
            exchange_name="test_knowledge_events",
            queue_prefix="test_kg_"
        )

    async def asyncTearDown(self):
        """Clean up test fixtures."""
        if self.event_bus.is_connected:
            await self.event_bus.disconnect()

    async def test_initialization(self):
        """Test that the event bus initializes correctly."""
        self.assertEqual(self.event_bus.connection_url, "amqp://guest:guest@localhost/")
        self.assertEqual(self.event_bus.exchange_name, "test_knowledge_events")
        self.assertEqual(self.event_bus.queue_prefix, "test_kg_")
        self.assertFalse(self.event_bus.is_connected)

    @patch('aio_pika.connect_robust')
    async def test_connect_success(self, mock_connect):
        """Test successful connection to RabbitMQ."""
        # Mock connection objects
        mock_connection = AsyncMock()
        mock_channel = AsyncMock()
        mock_exchange = AsyncMock()
        mock_rpc = AsyncMock()
        
        mock_connect.return_value = mock_connection
        mock_connection.channel.return_value = mock_channel
        mock_channel.set_qos.return_value = None
        mock_channel.declare_exchange.return_value = mock_exchange
        mock_channel.declare_queue.return_value = AsyncMock()
        mock_channel.bind.return_value = None
        
        # Mock RPC creation
        with patch('aio_pika.patterns.RPC.create', return_value=mock_rpc):
            await self.event_bus.connect()
        
        self.assertTrue(self.event_bus.is_connected)
        self.assertEqual(self.event_bus.connection, mock_connection)
        self.assertEqual(self.event_bus.channel, mock_channel)
        self.assertEqual(self.event_bus.exchange, mock_exchange)

    @patch('aio_pika.connect_robust')
    async def test_connect_failure(self, mock_connect):
        """Test connection failure handling."""
        mock_connect.side_effect = Exception("Connection failed")
        
        with self.assertRaises(Exception):
            await self.event_bus.connect()
        
        self.assertFalse(self.event_bus.is_connected)

    async def test_disconnect_not_connected(self):
        """Test disconnecting when not connected."""
        # Should not raise an error
        await self.event_bus.disconnect()
        self.assertFalse(self.event_bus.is_connected)

    @patch('aio_pika.connect_robust')
    async def test_disconnect_success(self, mock_connect):
        """Test successful disconnection."""
        # Mock connection objects
        mock_connection = AsyncMock()
        mock_channel = AsyncMock()
        mock_exchange = AsyncMock()
        mock_rpc = AsyncMock()
        
        mock_connect.return_value = mock_connection
        mock_connection.channel.return_value = mock_channel
        mock_channel.set_qos.return_value = None
        mock_channel.declare_exchange.return_value = mock_exchange
        
        # Mock RPC creation
        with patch('aio_pika.patterns.RPC.create', return_value=mock_rpc):
            await self.event_bus.connect()
        
        # Now disconnect
        await self.event_bus.disconnect()
        self.assertFalse(self.event_bus.is_connected)

    async def test_publish_local_fallback(self):
        """Test that publishing falls back to local handlers when not connected."""
        # Create a test event
        event = KnowledgeEvent(
            action="test_action",
            data={"test": "data"},
            role=Role.DATA_ENGINEER
        )
        
        # Mock handler
        handler_called = False
        handler_data = None
        
        async def test_handler(evt):
            nonlocal handler_called, handler_data
            handler_called = True
            handler_data = evt
        
        # Subscribe to the event
        await self.event_bus.subscribe("test_action", test_handler)
        
        # Publish event (should use local handlers)
        await self.event_bus.publish(event)
        
        # Verify handler was called
        self.assertTrue(handler_called)
        self.assertEqual(handler_data, event)

    @patch('aio_pika.connect_robust')
    async def test_publish_to_rabbitmq(self, mock_connect):
        """Test publishing to RabbitMQ when connected."""
        # Mock connection objects
        mock_connection = AsyncMock()
        mock_channel = AsyncMock()
        mock_exchange = AsyncMock()
        mock_rpc = AsyncMock()
        
        mock_connect.return_value = mock_connection
        mock_connection.channel.return_value = mock_channel
        mock_channel.set_qos.return_value = None
        mock_channel.declare_exchange.return_value = mock_exchange
        
        # Mock RPC creation
        with patch('aio_pika.patterns.RPC.create', return_value=mock_rpc):
            await self.event_bus.connect()
        
        # Create a test event
        event = KnowledgeEvent(
            action="test_action",
            data={"test": "data"},
            role=Role.DATA_ENGINEER
        )
        
        # Publish event
        await self.event_bus.publish(event)
        
        # Verify exchange.publish was called
        mock_exchange.publish.assert_called_once()
        
        # Verify message properties
        call_args = mock_exchange.publish.call_args
        message = call_args[0][0]  # First argument is the message
        self.assertEqual(message.content_type, "application/json")
        self.assertEqual(message.delivery_mode.value, 2)  # PERSISTENT

    @patch('aio_pika.connect_robust')
    async def test_subscribe_rabbitmq(self, mock_connect):
        """Test subscribing to RabbitMQ queues."""
        # Mock connection objects
        mock_connection = AsyncMock()
        mock_channel = AsyncMock()
        mock_exchange = AsyncMock()
        mock_rpc = AsyncMock()
        mock_queue = AsyncMock()
        
        mock_connect.return_value = mock_connection
        mock_connection.channel.return_value = mock_channel
        mock_channel.set_qos.return_value = None
        mock_channel.declare_exchange.return_value = mock_exchange
        mock_channel.declare_queue.return_value = mock_queue
        mock_channel.bind.return_value = None
        
        # Mock RPC creation
        with patch('aio_pika.patterns.RPC.create', return_value=mock_rpc):
            await self.event_bus.connect()
        
        # Subscribe to an event type
        async def test_handler(event):
            pass
        
        await self.event_bus.subscribe("test_event_type", test_handler)
        
        # Verify queue was declared
        mock_channel.declare_queue.assert_called_once()
        mock_channel.bind.assert_called_once()
        
        # Verify consumer task was created
        self.assertEqual(len(self.event_bus._consumer_tasks), 1)

    async def test_health_check_not_connected(self):
        """Test health check when not connected."""
        health = await self.event_bus.health_check()
        self.assertEqual(health["status"], "disconnected")
        self.assertIn("error", health)

    @patch('aio_pika.connect_robust')
    async def test_health_check_connected(self, mock_connect):
        """Test health check when connected."""
        # Mock connection objects
        mock_connection = AsyncMock()
        mock_channel = AsyncMock()
        mock_exchange = AsyncMock()
        mock_rpc = AsyncMock()
        
        mock_connect.return_value = mock_connection
        mock_connection.channel.return_value = mock_channel
        mock_channel.set_qos.return_value = None
        mock_channel.declare_exchange.return_value = mock_exchange
        
        # Mock RPC creation
        with patch('aio_pika.patterns.RPC.create', return_value=mock_rpc):
            await self.event_bus.connect()
        
        # Set connection and channel as not closed
        mock_connection.is_closed = False
        mock_channel.is_closed = False
        
        health = await self.event_bus.health_check()
        self.assertEqual(health["status"], "healthy")
        self.assertEqual(health["connection"], "connected")
        self.assertEqual(health["channel"], "open")

    @patch('aio_pika.connect_robust')
    async def test_get_queue_info(self, mock_connect):
        """Test getting queue information."""
        # Mock connection objects
        mock_connection = AsyncMock()
        mock_channel = AsyncMock()
        mock_exchange = AsyncMock()
        mock_rpc = AsyncMock()
        mock_queue = AsyncMock()
        
        mock_connect.return_value = mock_connection
        mock_connection.channel.return_value = mock_channel
        mock_channel.set_qos.return_value = None
        mock_channel.declare_exchange.return_value = mock_exchange
        mock_channel.declare_queue.return_value = mock_queue
        
        # Mock RPC creation
        with patch('aio_pika.patterns.RPC.create', return_value=mock_rpc):
            await self.event_bus.connect()
        
        # Mock queue declaration result
        mock_declaration_result = Mock()
        mock_declaration_result.message_count = 5
        mock_declaration_result.consumer_count = 2
        mock_queue.declaration_result = mock_declaration_result
        
        queue_info = await self.event_bus.get_queue_info("test_event")
        
        self.assertEqual(queue_info["event_type"], "test_event")
        self.assertEqual(queue_info["message_count"], 5)
        self.assertEqual(queue_info["consumer_count"], 2)

    async def test_publish_batch_local_fallback(self):
        """Test batch publishing falls back to local handlers when not connected."""
        # Create test events
        events = [
            KnowledgeEvent(action="action1", data={"id": "1"}, role=Role.DATA_ENGINEER),
            KnowledgeEvent(action="action2", data={"id": "2"}, role=Role.DATA_ENGINEER)
        ]
        
        # Mock handler
        handler_calls = []
        
        async def test_handler(event):
            handler_calls.append(event.action)
        
        # Subscribe to both event types
        await self.event_bus.subscribe("action1", test_handler)
        await self.event_bus.subscribe("action2", test_handler)
        
        # Publish batch
        await self.event_bus.publish_batch(events)
        
        # Verify both handlers were called
        self.assertEqual(len(handler_calls), 2)
        self.assertIn("action1", handler_calls)
        self.assertIn("action2", handler_calls)

    @patch('aio_pika.connect_robust')
    async def test_rpc_functionality(self, mock_connect):
        """Test RPC functionality when connected."""
        # Mock connection objects
        mock_connection = AsyncMock()
        mock_channel = AsyncMock()
        mock_exchange = AsyncMock()
        mock_rpc = AsyncMock()
        
        mock_connect.return_value = mock_connection
        mock_connection.channel.return_value = mock_channel
        mock_channel.set_qos.return_value = None
        mock_channel.declare_exchange.return_value = mock_exchange
        
        # Mock RPC creation
        with patch('aio_pika.patterns.RPC.create', return_value=mock_rpc):
            await self.event_bus.connect()
        
        # Test RPC call
        mock_response = Mock()
        mock_response.body = b'{"result": "success"}'
        mock_rpc.call.return_value = mock_response
        
        result = await self.event_bus.call_rpc("test_method", {"param": "value"})
        
        self.assertEqual(result, {"result": "success"})
        mock_rpc.call.assert_called_once()

    @patch('aio_pika.connect_robust')
    async def test_register_rpc_handler(self, mock_connect):
        """Test registering RPC handlers."""
        # Mock connection objects
        mock_connection = AsyncMock()
        mock_channel = AsyncMock()
        mock_exchange = AsyncMock()
        mock_rpc = AsyncMock()
        
        mock_connect.return_value = mock_connection
        mock_connection.channel.return_value = mock_channel
        mock_channel.set_qos.return_value = None
        mock_channel.declare_exchange.return_value = mock_exchange
        
        # Mock RPC creation
        with patch('aio_pika.patterns.RPC.create', return_value=mock_rpc):
            await self.event_bus.connect()
        
        # Test RPC handler registration
        async def test_rpc_handler(data):
            return {"processed": data}
        
        await self.event_bus.register_rpc_handler("test_method", test_rpc_handler)
        
        mock_rpc.register.assert_called_once()


if __name__ == "__main__":
    unittest.main()
