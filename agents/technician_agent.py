from praisonai.agents_generator import PraisonAgent as PraisonAIAgent
from praisonai.agents_generator import PraisonTask as Task
from tools.scientific_tools import ScientificTools

class TechnicianAgent:
    def __init__(self, llm):
        self.llm = llm
        self.agent = PraisonAIAgent(
            role='Virtual Lab Technician',
            goal='Execute the Python experiment code in a secure, simulated environment.',
            backstory=(
                "You are responsible for running the computational experiments. You ensure the code runs "
                "correctly and report the outcome, be it success or an error."
            ),
            tools=[ScientificTools.execute_python_code],
            llm=self.llm
        )

    def get_task(self) -> Task:
        return Task(
            agent=self.agent,
            description=(
                "Take the Python script provided by the Experiment Designer and execute it using the `execute_python_code` tool. "
                "Report the outcome of the execution."
            )
        )
