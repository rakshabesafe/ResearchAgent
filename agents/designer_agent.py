from praisonai.agents_generator import PraisonAgent as PraisonAIAgent
from praisonai.agents_generator import PraisonTask as Task

class DesignerAgent:
    def __init__(self, llm):
        self.llm = llm
        self.agent = PraisonAIAgent(
            role='Computational Experiment Designer',
            goal='Design a detailed, executable Python experiment to test a given hypothesis.',
            backstory=(
                "You are a meticulous programmer with a deep understanding of scientific methodology. "
                "You translate abstract hypotheses into concrete, reproducible Python code for simulation."
            ),
            # This agent doesn't need external tools; its output is code as text.
            llm=self.llm
        )

    def get_task(self) -> Task:
        return Task(
            agent=self.agent,
            description=(
                "Based on the hypothesis from the researcher, design a Python script for a computational experiment. "
                "The script should:\n"
                "- Generate 100 hypothetical molecular structures using a mock GNN model.\n"
                "- Simulate the prediction of 'binding_affinity' and 'toxicity_score' for each.\n"
                "- Save the results to a CSV file named 'results.csv'.\n"
                "Provide only the complete, runnable Python code as your final output."
            )
        )
