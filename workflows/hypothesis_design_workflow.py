from agents.researcher_agent import ResearcherAgent
from agents.designer_agent import DesignerAgent
from praisonaiagents import Task # Needed for type hinting if we add it

class HypothesisDesignWorkflow:
    def __init__(self, researcher_agent: ResearcherAgent, designer_agent: DesignerAgent):
        self.researcher_agent = researcher_agent
        self.designer_agent = designer_agent

    def get_tasks(self, research_topic: str) -> list[Task]:
        """
        Generates the sequence of tasks for hypothesis formulation and experiment design.
        """
        task_hypothesis = self.researcher_agent.get_task(research_topic)
        task_design = self.designer_agent.get_task()

        # The design task depends on the output of the hypothesis task.
        # PraisonAI handles this dependency automatically if tasks are correctly defined
        # and their agents are part of the same crew.
        # If explicit dependency management is needed, it would be set here.
        # For example: task_design.context = [task_hypothesis]
        # However, PraisonAI usually infers this from task order and agent outputs.

        return [task_hypothesis, task_design]
