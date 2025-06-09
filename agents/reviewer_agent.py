from praisonaiagents import Agent as PraisonAIAgent
from praisonaiagents import Task

class ReviewerAgent:
    def __init__(self, llm):
        self.llm = llm
        self.agent = PraisonAIAgent(
            role='Peer Reviewer',
            goal='Critically review the generated scientific paper for clarity, soundness, and contribution.',
            backstory=(
                "You are a discerning critic with a keen eye for detail. You review scientific work "
                "to identify weaknesses, suggest improvements, and ensure the final output meets "
                "high academic standards."
            ),
            # No external tools needed for this agent.
            llm=self.llm
        )

    def get_task(self) -> Task:
        return Task(
            agent=self.agent,
            description=(
                "Critically review the draft of the scientific paper. "
                "Provide constructive feedback focusing on:\n"
                "- Clarity of the hypothesis.\n"
                "- Soundness of the reported results.\n"
                "- Overall contribution.\n"
                "Finally, provide a revised, improved version of the paper as your final output."
            )
        )
