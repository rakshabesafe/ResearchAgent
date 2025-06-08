from agents.analyst_agent import AnalystAgent
from agents.writer_agent import WriterAgent
from praisonai.agents_generator import PraisonTask as Task # Needed for type hinting

class AnalysisAndWritingWorkflow:
    def __init__(self, analyst_agent: AnalystAgent, writer_agent: WriterAgent):
        self.analyst_agent = analyst_agent
        self.writer_agent = writer_agent

    def get_tasks(self) -> list[Task]:
        """
        Generates the sequence of tasks for data analysis and paper writing.
        """
        task_analyze = self.analyst_agent.get_task()
        task_write = self.writer_agent.get_task()

        # PraisonAI handles dependencies based on task order and agent outputs.
        # task_write will use the output of task_analyze.

        return [task_analyze, task_write]
