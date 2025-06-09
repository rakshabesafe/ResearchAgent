from praisonaiagents import Agent as PraisonAIAgent
from praisonaiagents import Task
from tools.scientific_tools import ScientificTools

class AnalystAgent:
    def __init__(self, llm):
        self.llm = llm
        self.agent = PraisonAIAgent(
            role='Data Scientist and Analyst',
            goal='Analyze the results of the experiment to extract meaningful insights.',
            backstory=(
                "You are a master of statistical analysis and data visualization. "
                "You can find the signal in the noise, turning raw experimental data "
                "into clear, concise findings."
            ),
            tools=[ScientificTools.analyze_data],
            llm=self.llm
        )

    def get_task(self) -> Task:
        return Task(
            agent=self.agent,
            description=(
                "The experiment generated a file at 'results.csv'.\n"
                "Analyze this file using the `analyze_data` tool to summarize the key findings."
            )
        )
