# AI Scientist Framework using PraisonAI
# This script implements the high-level design for an autonomous research agent.
# ... (rest of the header comments)

import os
import asyncio # Keep asyncio as PraisonAI/LiteLLM might use it internally

from praisonai import PraisonAI
from praisonai.agents_generator import PraisonAgent as PraisonAIAgent
from praisonai.agents_generator import PraisonTask as Task

from tools.scientific_tools import ScientificTools
# MCP related imports removed

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
llm_provider = os.environ.get("LLM_PROVIDER", "openai").lower()
llm_config_params = {}

print(f"--- Configuring LLM for provider: {llm_provider} ---")

if llm_provider == "ollama":
    ollama_model_name = os.environ.get("OLLAMA_MODEL_NAME")
    if not ollama_model_name:
        raise ValueError("OLLAMA_MODEL_NAME environment variable must be set when LLM_PROVIDER is 'ollama'.")
    if os.environ.get("OLLAMA_API_BASE"):
        print(f"Using Ollama. Model: '{ollama_model_name}' (set via OLLAMA_MODEL_NAME env var). API Base: '{os.environ.get('OLLAMA_API_BASE')}' (set via OLLAMA_API_BASE env var).")
    else:
        print(f"Using Ollama. Model: '{ollama_model_name}' (set via OLLAMA_MODEL_NAME env var). OLLAMA_API_BASE not set (LiteLLM will use default).")

elif llm_provider == "openai":
    if not os.environ.get("OPENAI_API_KEY"):
        print("OPENAI_API_KEY not found, using placeholder key.")
        os.environ["OPENAI_API_KEY"] = "sk-your_api_key_here" # Placeholder
    openai_model_name = os.environ.get("OPENAI_MODEL_NAME", "gpt-3.5-turbo")
    print(f"Using OpenAI (model specified by OPENAI_MODEL_NAME env var: {openai_model_name} or LiteLLM default)")
else:
    raise ValueError(f"Unsupported LLM_PROVIDER: '{llm_provider}'. Must be 'openai' or 'ollama'.")

llm_object_for_agents = PraisonAI(**llm_config_params)
print("--- LLM Configuration Complete ---")

# --- MCP Setup Removed ---
# MCPClientManager instantiation removed
# atexit registration removed
# _run_async_cleanup function removed
# MCP_TOOLS_CONFIG list removed

# --- Agent Instantiation ---
researcher_agent_instance = ResearcherAgent(llm=llm_object_for_agents)
designer_agent_instance = DesignerAgent(llm=llm_object_for_agents)
technician_agent_instance = TechnicianAgent(llm=llm_object_for_agents)
analyst_agent_instance = AnalystAgent(llm=llm_object_for_agents)
writer_agent_instance = WriterAgent(llm=llm_object_for_agents)
reviewer_agent_instance = ReviewerAgent(llm=llm_object_for_agents)

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

    tasks_hd = hypothesis_design_wf.get_tasks(research_topic)
    tasks_ex = execution_wf.get_tasks()
    tasks_aw = analysis_writing_wf.get_tasks()
    tasks_rev = review_wf.get_tasks()
    all_tasks = tasks_hd + tasks_ex + tasks_aw + tasks_rev

    print("--- Attempting to run main PraisonAI crew using llm_object_for_agents.main() ---")
    final_manuscript = llm_object_for_agents.main()

    print("\n\n✅ AI Scientist Framework execution complete!")
    print("="*50)
    print("Final Manuscript (as approved by Peer Reviewer):")
    print(final_manuscript)
    print("="*50)

    # --- MCP Test Section Removed ---
    # _run_mcp_direct_test function removed
    # asyncio.run call for MCP test removed
    # All print statements related to MCP test removed
    print("\n--- MCP Test Section Fully Removed ---") # Placeholder to confirm removal in output
