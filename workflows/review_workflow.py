from agents.reviewer_agent import ReviewerAgent
from praisonai import Task # Needed for type hinting

class ReviewWorkflow:
    def __init__(self, reviewer_agent: ReviewerAgent):
        self.reviewer_agent = reviewer_agent

    def get_tasks(self) -> list[Task]:
        """
        Generates the sequence of tasks for paper review.
        """
        task_review = self.reviewer_agent.get_task()

        # This task depends on the output of the writing task.
        # PraisonAI handles this dependency automatically.

        return [task_review]
