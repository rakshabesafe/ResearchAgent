from praisonai.agents_generator import PraisonAgent as PraisonAIAgent
from praisonai.agents_generator import PraisonTask as Task
from tools.scientific_tools import ScientificTools

class WriterAgent:
    def __init__(self, llm):
        self.llm = llm
        self.agent = PraisonAIAgent(
            role='Scientific Writer',
            goal='Write a complete, well-structured scientific paper based on the experimental findings.',
            backstory=(
                "You are a skilled communicator who can articulate complex scientific results "
                "in the formal structure of an academic paper. You draft the abstract, "
                "introduction, methods, results, and conclusion."
            ),
            tools=[ScientificTools.write_latex_paper],
            llm=self.llm
        )

    def get_task(self) -> Task:
        return Task(
            agent=self.agent,
            description=(
                "Take the data analysis summary and the original hypothesis. "
                "Use the `write_latex_paper` tool to generate a full draft of a scientific paper."
            )
        )
