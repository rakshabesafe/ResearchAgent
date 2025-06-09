from agents.technician_agent import TechnicianAgent
from praisonaiagents import Task # Needed for type hinting

class ExecutionWorkflow:
    def __init__(self, technician_agent: TechnicianAgent):
        self.technician_agent = technician_agent

    def get_tasks(self) -> list[Task]:
        """
        Generates the sequence of tasks for experiment execution.
        """
        task_execute = self.technician_agent.get_task()

        # This task typically depends on the output of a design task.
        # PraisonAI handles this dependency automatically through sequential task processing
        # when tasks are added to the main list in the correct order.

        return [task_execute]
