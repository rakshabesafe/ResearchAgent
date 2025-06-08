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
from praisonai import PraisonAI, PraisonAIAgent, Task # PraisonAIAgent, Task for context
from tools.scientific_tools import ScientificTools

# Agent imports
from agents.researcher_agent import ResearcherAgent
from agents.designer_agent import DesignerAgent
from agents.technician_agent import TechnicianAgent
from agents.analyst_agent import AnalystAgent
from agents.writer_agent import WriterAgent
from agents.reviewer_agent import ReviewerAgent

# Workflow imports
from workflows.hypothesis_design_workflow import HypothesisDesignWorkflow
from workflows.execution_workflow import ExecutionWorkflow
from workflows.analysis_writing_workflow import AnalysisAndWritingWorkflow
from workflows.review_workflow import ReviewWorkflow

# --- LLM Configuration for Agents ---
# Set up the LLM. PraisonAI uses LiteLLM to support 100+ models.
# By default, it will look for OPENAI_API_KEY.
# If you want to use another model (e.g., Groq, Anthropic), set the corresponding env variables.
# For this example, we'll use a placeholder if no key is found.
if not os.environ.get("OPENAI_API_KEY"):
    os.environ["OPENAI_API_KEY"] = "sk-your_api_key_here"

# This PraisonAI instance is used to configure the LLM for individual agents
llm_object_for_agents = PraisonAI()

# --- Agent Instantiation ---
researcher_agent_instance = ResearcherAgent(llm=llm_object_for_agents)
designer_agent_instance = DesignerAgent(llm=llm_object_for_agents)
technician_agent_instance = TechnicianAgent(llm=llm_object_for_agents)
analyst_agent_instance = AnalystAgent(llm=llm_object_for_agents)
writer_agent_instance = WriterAgent(llm=llm_object_for_agents)
reviewer_agent_instance = ReviewerAgent(llm=llm_object_for_agents)

# Collect all underlying PraisonAIAgent instances for the main crew
all_agents_instances = [
    researcher_agent_instance.agent,
    designer_agent_instance.agent,
    technician_agent_instance.agent,
    analyst_agent_instance.agent,
    writer_agent_instance.agent,
    reviewer_agent_instance.agent
]

# --- Workflow Instantiation ---
hypothesis_design_wf = HypothesisDesignWorkflow(researcher_agent_instance, designer_agent_instance)
execution_wf = ExecutionWorkflow(technician_agent_instance)
analysis_writing_wf = AnalysisAndWritingWorkflow(analyst_agent_instance, writer_agent_instance)
review_wf = ReviewWorkflow(reviewer_agent_instance)

# --- Research Topic ---
research_topic = "Using Graph Neural Networks to discover molecules with high binding affinity and low toxicity."

# --- Main Orchestration ---
if __name__ == "__main__":
    print("🚀 Kicking off the AI Scientist Framework...")
    print(f"Research Topic: {research_topic}\n")

    # Collect Tasks from Workflows
    tasks_hd = hypothesis_design_wf.get_tasks(research_topic)
    tasks_ex = execution_wf.get_tasks()
    tasks_aw = analysis_writing_wf.get_tasks()
    tasks_rev = review_wf.get_tasks()

    all_tasks = tasks_hd + tasks_ex + tasks_aw + tasks_rev

    # Create and run the main crew
    # This PraisonAI instance is the main orchestrator
    crew_orchestrator = PraisonAI(agents=all_agents_instances, tasks=all_tasks)

    final_manuscript = crew_orchestrator.main()

    print("\n\n✅ AI Scientist Framework execution complete!")
    print("="*50)
    print("Final Manuscript (as approved by Peer Reviewer):")
    print("="*50)
    print(final_manuscript)
