from praisonai import PraisonAIAgent, Task
from tools.scientific_tools import ScientificTools

class ResearcherAgent:
    def __init__(self, llm):
        self.llm = llm
        self.agent = PraisonAIAgent(
            role='Senior Scientific Researcher',
            goal='Identify promising, unexplored research directions in computational drug discovery.',
            backstory=(
                "You are an expert in bioinformatics and computational chemistry. "
                "Your mission is to scour scientific literature to find knowledge gaps "
                "and formulate novel, testable hypotheses."
            ),
            tools=[ScientificTools.search_arxiv],
            llm=self.llm
        )

    def get_task(self, research_topic: str) -> Task:
        return Task(
            agent=self.agent,
            description=(
                f"1. Search for recent papers on the topic: '{research_topic}'.\n"
                "2. Analyze the findings and identify a gap in the current research.\n"
                "3. Formulate a single, clear, and testable hypothesis based on this gap."
            )
        )
