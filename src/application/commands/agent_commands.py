from dataclasses import dataclass

from application.agent_runner import AgentRunner
from application.commands.base import Command, CommandHandler


@dataclass(frozen=True)
class RunAgentCommand(Command):
    role: str


@dataclass(frozen=True)
class StartProjectCommand(Command):
    project_goal: str


class RunAgentHandler(CommandHandler):
    """
    Handles the execution of an agent based on its role.
    """

    def __init__(self, agent_runner: AgentRunner):
        self.agent_runner = agent_runner

    async def handle(self, command: RunAgentCommand) -> None:
        """
        Starts the agent runner.

        This will block until the runner is stopped or cancelled.
        """
        print(f"Handler received command to run agent with role: {command.role}")
        await self.agent_runner.run()
