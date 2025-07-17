from application.commands.base import CommandHandler
from application.commands.collaboration_commands import BuildKGCommand

class BuildKGCommandHandler(CommandHandler[BuildKGCommand]):
    """
    Handles the command to build a knowledge graph.
    """
    async def handle(self, command: BuildKGCommand) -> None:
        print(f"Data Engineer received command to build KG from: {command.metadata_uri}")
        # In a real implementation, this handler would:
        # 1. Read the metadata from the URI.
        # 2. Process it into nodes and relationships.
        # 3. Use the GraphRepository to persist the graph.
        pass 