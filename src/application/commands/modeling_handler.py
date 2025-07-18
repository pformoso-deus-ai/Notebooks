from application.commands.base import CommandHandler
from application.commands.modeling_command import ModelingCommand
from application.agents.data_architect.modeling_workflow import ModelingWorkflow, ModelingResult


class ModelingCommandHandler(CommandHandler):
    """Handles ModelingCommand execution."""
    
    def __init__(self, modeling_workflow: ModelingWorkflow):
        self.modeling_workflow = modeling_workflow
    
    async def handle(self, command: ModelingCommand) -> ModelingResult:
        """Execute the modeling workflow."""
        try:
            result = await self.modeling_workflow.execute(command)
            return result
        except Exception as e:
            return ModelingResult(
                success=False,
                errors=[f"Modeling workflow failed: {str(e)}"]
            ) 