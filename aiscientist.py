# AI Scientist Framework using PraisonAI
# This script implements the high-level design for an autonomous research agent.
#
# To run this code:
# 1. Make sure you have Python installed.
# 2. Install the PraisonAI library:
#    pip install praisonai
# 3. Set your LLM API key as an environment variable. For example, for OpenAI:
#    export OPENAI_API_KEY='your_api_key_here'
#    (The script will default to a placeholder if no key is found)

import os
from praisonai import PraisonAI, PraisonAIAgent, Task

# --- 1. Tool Definitions ---
# In a real-world scenario, these tools would perform complex actions like
# searching academic databases, running code in a secure sandbox, etc.
# For this demonstration, we are creating mock tools that simulate the output.

class ScientificTools:
    """A collection of mock tools for our AI Scientist agents."""

    @staticmethod
    def search_arxiv(query: str) -> str:
        """
        Simulates searching the arXiv database for a given query.
        Returns a mock list of relevant papers.
        """
        print(f"\n MOCK TOOL: Searching ArXiv for '{query}'...")
        return (
            "Found Papers:\n"
            "- 'The role of Graph Neural Networks in molecular design' (2023)\n"
            "- 'Advancements in protein folding prediction using Transformers' (2022)\n"
            "- 'A survey of generative models for drug discovery' (2024)"
        )

    @staticmethod
    def execute_python_code(code: str) -> str:
        """
        Simulates executing Python code in a sandboxed environment.
        Returns a mock result of the execution.
        """
        print(f"\n MOCK TOOL: Executing Python code in a sandbox...")
        # print("--- CODE ---\n" + code + "\n------------")
        # In a real implementation, NEVER use exec() on LLM-generated code
        # without extreme sandboxing and security measures.
        return "Execution successful. Data saved to 'results.csv'.\nColumns: 'molecule_id', 'binding_affinity', 'toxicity_score'"

    @staticmethod
    def analyze_data(file_path: str) -> str:
        """
        Simulates analyzing a data file.
        Returns a mock summary of the analysis.
        """
        print(f"\n MOCK TOOL: Analyzing data from '{file_path}'...")
        return (
            "Data Analysis Summary:\n"
            "- 25 out of 100 tested molecules show high binding affinity (>0.9).\n"
            "- A positive correlation was found between molecular weight and toxicity.\n"
            "- Molecule 'MOL-012' shows the most promise with high affinity and low toxicity."
        )

    @staticmethod
    def write_latex_paper(analysis_summary: str, hypothesis: str) -> str:
        """
        Simulates writing a scientific paper in LaTeX format.
        """
        print("\n MOCK TOOL: Compiling analysis into a LaTeX paper draft...")
        return f"""
\\documentclass{{article}}
\\title{{A Study on Novel Molecules for Drug Discovery}}
\\author{{AI Scientist Framework}}
\\begin{document}
\\maketitle

\\section*{{Abstract}}
This paper investigates novel molecular structures based on the hypothesis that {hypothesis}. Our computational analysis reveals several promising candidates for further study.

\\section{{Introduction}}
The search for effective and non-toxic drugs is a significant challenge in modern medicine. This work explores...

\\section{{Methodology}}
We designed a computational experiment to generate and evaluate 100 novel molecules based on our initial hypothesis.

\\section{{Results}}
Our analysis of the experimental data reveals the following key findings:
{analysis_summary}

\\section{{Conclusion}}
The results support our initial hypothesis. Specifically, molecule 'MOL-012' warrants further in-vitro testing.

\\end{{document}}
"""

# --- 2. Agent Definitions ---
# We define a "crew" of agents, each with a specific role, goal, and set of tools.
# The orchestrator role is implicitly handled by the `Crew` object in PraisonAI.

# Set up the LLM. PraisonAI uses LiteLLM to support 100+ models.
# By default, it will look for OPENAI_API_KEY.
# If you want to use another model (e.g., Groq, Anthropic), set the corresponding env variables.
# For this example, we'll use a placeholder if no key is found.
if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = "sk-your_api_key_here"

llm = PraisonAI()

# Agent 1: The Researcher
researcher = PraisonAIAgent(
    role='Senior Scientific Researcher',
    goal='Identify promising, unexplored research directions in computational drug discovery.',
    backstory=(
        "You are an expert in bioinformatics and computational chemistry. "
        "Your mission is to scour scientific literature to find knowledge gaps "
        "and formulate novel, testable hypotheses."
    ),
    tools=[ScientificTools.search_arxiv],
    llm=llm
)

# Agent 2: The Experiment Designer
designer = PraisonAIAgent(
    role='Computational Experiment Designer',
    goal='Design a detailed, executable Python experiment to test a given hypothesis.',
    backstory=(
        "You are a meticulous programmer with a deep understanding of scientific methodology. "
        "You translate abstract hypotheses into concrete, reproducible Python code for simulation."
    ),
    # This agent doesn't need external tools; its output is code as text.
    llm=llm
)

# Agent 3: The Lab Technician (Execution Agent)
technician = PraisonAIAgent(
    role='Virtual Lab Technician',
    goal='Execute the Python experiment code in a secure, simulated environment.',
    backstory=(
        "You are responsible for running the computational experiments. You ensure the code runs "
        "correctly and report the outcome, be it success or an error."
    ),
    tools=[ScientificTools.execute_python_code],
    llm=llm
)

# Agent 4: The Data Analyst
analyst = PraisonAIAgent(
    role='Data Scientist and Analyst',
    goal='Analyze the results of the experiment to extract meaningful insights.',
    backstory=(
        "You are a master of statistical analysis and data visualization. "
        "You can find the signal in the noise, turning raw experimental data "
        "into clear, concise findings."
    ),
    tools=[ScientificTools.analyze_data],
    llm=llm
)

# Agent 5: The Writer
writer = PraisonAIAgent(
    role='Scientific Writer',
    goal='Write a complete, well-structured scientific paper based on the experimental findings.',
    backstory=(
        "You are a skilled communicator who can articulate complex scientific results "
        "in the formal structure of an academic paper. You draft the abstract, "
        "introduction, methods, results, and conclusion."
    ),
    tools=[ScientificTools.write_latex_paper],
    llm=llm
)

# Agent 6: The Reviewer
reviewer = PraisonAIAgent(
    role='Peer Reviewer',
    goal='Critically review the generated scientific paper for clarity, soundness, and contribution.',
    backstory=(
        "You are a discerning critic with a keen eye for detail. You review scientific work "
        "to identify weaknesses, suggest improvements, and ensure the final output meets "
        "high academic standards."
    ),
    # No external tools needed for this agent.
    llm=llm
)

# --- 3. Task Definitions ---
# We define the sequence of tasks that the agents will perform.
# The output of each task is automatically passed as context to the next.

research_topic = "Using Graph Neural Networks to discover molecules with high binding affinity and low toxicity."

# Task 1: Formulate Hypothesis
task_hypothesis = Task(
    agent=researcher,
    description=(
        f"1. Search for recent papers on the topic: '{research_topic}'.\n"
        "2. Analyze the findings and identify a gap in the current research.\n"
        "3. Formulate a single, clear, and testable hypothesis based on this gap."
    )
)

# Task 2: Design Experiment
task_design = Task(
    agent=designer,
    description=(
        "Based on the hypothesis from the researcher, design a Python script for a computational experiment. "
        "The script should:\n"
        "- Generate 100 hypothetical molecular structures using a mock GNN model.\n"
        "- Simulate the prediction of 'binding_affinity' and 'toxicity_score' for each.\n"
        "- Save the results to a CSV file named 'results.csv'.\n"
        "Provide only the complete, runnable Python code as your final output."
    )
)

# Task 3: Execute Experiment
task_execute = Task(
    agent=technician,
    description=(
        "Take the Python script provided by the Experiment Designer and execute it using the `execute_python_code` tool. "
        "Report the outcome of the execution."
    )
)

# Task 4: Analyze Results
task_analyze = Task(
    agent=analyst,
    description=(
        "The experiment generated a file at 'results.csv'.\n"
        "Analyze this file using the `analyze_data` tool to summarize the key findings."
    )
)

# Task 5: Write Paper
task_write = Task(
    agent=writer,
    description=(
        "Take the data analysis summary and the original hypothesis. "
        "Use the `write_latex_paper` tool to generate a full draft of a scientific paper."
    )
)

# Task 6: Review and Refine
task_review = Task(
    agent=reviewer,
    description=(
        "Critically review the draft of the scientific paper. "
        "Provide constructive feedback focusing on:\n"
        "- Clarity of the hypothesis.\n"
        "- Soundness of the reported results.\n"
        "- Overall contribution.\n"
        "Finally, provide a revised, improved version of the paper as your final output."
    )
)


# --- 4. Orchestration ---
# We assemble the crew and kick off the process.

# PraisonAI's `main` function is a convenient way to run the crew.
# It takes the list of agents and tasks and executes them sequentially.
if __name__ == "__main__":
    print("🚀 Kicking off the AI Scientist Framework...")
    print(f"Research Topic: {research_topic}\n")

    # Assemble the crew and their tasks
    crew = PraisonAI(
        agents=[researcher, designer, technician, analyst, writer, reviewer],
        tasks=[task_hypothesis, task_design, task_execute, task_analyze, task_write, task_review],
    )

    # Run the simulation
    final_manuscript = crew.main()

    print("\n\n✅ AI Scientist Framework execution complete!")
    print("="*50)
    print("Final Manuscript (as approved by Peer Reviewer):")
    print("="*50)
    print(final_manuscript)

