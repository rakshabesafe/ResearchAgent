# AI Scientist Framework using PraisonAI
# This script implements the high-level design for an autonomous research agent.
# ... (rest of the header comments)

import os
import asyncio # Keep asyncio as PraisonAI/LiteLLM might use it internally

from praisonaiagents import PraisonAIAgents as Workflow
from praisonaiagents import Agent as PraisonAIAgent
from praisonaiagents import Task

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

# Determine the LLM configuration to be passed to individual agent instances
agent_llm_config = None
if llm_provider == "ollama":
    agent_llm_config = os.environ.get("OLLAMA_MODEL_NAME")
    # If praisonaiagents.Agent expects a dict, this might be:
    # agent_llm_config = {
    #     "model": os.environ.get("OLLAMA_MODEL_NAME"),
    #     "api_base": os.environ.get("OLLAMA_API_BASE"),
    #     # Potentially "api_key": "not-needed" or actual key if required by specific ollama setup with LiteLLM
    # }
elif llm_provider == "openai":
    # Pass a dictionary to ensure api_key is explicitly included for LiteLLM
    agent_llm_config = {
        "model": os.environ.get("OPENAI_MODEL_NAME", "gpt-3.5-turbo"),
        "api_key": os.environ.get("OPENAI_API_KEY", "not-needed") # Ensure OPENAI_API_KEY is included
    }
    # If an API base is needed (e.g. for local OpenAI compatible server), add it here:
    # if os.environ.get("OPENAI_API_BASE"):
    #    agent_llm_config["api_base"] = os.environ.get("OPENAI_API_BASE")

print(f"--- Agent LLM Config determined: {agent_llm_config} ---")
print("--- LLM Configuration for Agents Complete ---") # End of LLM config block

# --- MCP Setup Removed ---
# MCPClientManager instantiation removed
# atexit registration removed
# _run_async_cleanup function removed
# MCP_TOOLS_CONFIG list removed

# --- Agent Instantiation (must happen before Workflow instantiation) ---
# The 'llm' parameter for these custom agent classes will now be the agent_llm_config
researcher_agent_instance = ResearcherAgent(llm=agent_llm_config)
designer_agent_instance = DesignerAgent(llm=agent_llm_config)
technician_agent_instance = TechnicianAgent(llm=agent_llm_config)
analyst_agent_instance = AnalystAgent(llm=agent_llm_config)
writer_agent_instance = WriterAgent(llm=agent_llm_config)
reviewer_agent_instance = ReviewerAgent(llm=agent_llm_config)

all_agents_instances = [
    researcher_agent_instance.agent, # Assuming .agent gives the PraisonAIAgent (praisonaiagents.Agent) instance
    designer_agent_instance.agent,
    technician_agent_instance.agent,
    analyst_agent_instance.agent,
    writer_agent_instance.agent,
    reviewer_agent_instance.agent
]

# --- Workflow Instantiation (now with agents) ---
# llm_config_params is currently empty. If Workflow needs specific LLM settings beyond agents,
# this might need to be populated from llm_provider logic too.
llm_object_for_agents = Workflow(agents=all_agents_instances, process="workflow", **llm_config_params)
print("--- Main Workflow Object Instantiated ---")

# --- Workflow Definitions (associating agents with their roles in these conceptual workflows) ---
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

    print("--- Attempting to run main PraisonAI crew using llm_object_for_agents.start() ---")
    final_manuscript = llm_object_for_agents.start()

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
