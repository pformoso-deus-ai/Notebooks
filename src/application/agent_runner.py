import asyncio

from domain.agent import Agent


class AgentRunner:
    """
    Handles the execution loop for an agent.
    """

    def __init__(self, agent: Agent, loop_interval: float = 1.0):
        """
        Initializes the runner.

        Args:
            agent: The agent instance to run.
            loop_interval: The time in seconds to wait between message checks.
        """
        self.agent = agent
        self.loop_interval = loop_interval
        self._is_running = False

    async def run(self) -> None:
        """
        Starts the main processing loop for the agent.
        """
        self._is_running = True
        print(f"Agent runner for '{self.agent.agent_id}' started.")
        while self._is_running:
            try:
                await self.agent.process_messages()
                await asyncio.sleep(self.loop_interval)
            except asyncio.CancelledError:
                print(f"Agent runner for '{self.agent.agent_id}' was cancelled.")
                break
            except Exception as e:
                print(f"An error occurred in agent '{self.agent.agent_id}': {e}")
                # Depending on the desired robustness, you might want to
                # add more sophisticated error handling or backoff strategies here.

    def stop(self) -> None:
        """
        Stops the agent's processing loop.
        """
        self._is_running = False
        print(f"Agent runner for '{self.agent.agent_id}' stopping.")
