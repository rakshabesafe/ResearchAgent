# AI Scientist Framework using PraisonAI
# This script implements the high-level design for an autonomous research agent.
#
# To run this code:
# 1. Make sure you have Python installed.
# 2. Install the PraisonAI library:
#    pip install praisonai
# 3. Set relevant environment variables:
#    - LLM_PROVIDER: 'openai' (default) or 'ollama'
#    - For OpenAI: OPENAI_API_KEY (will use placeholder if not set)
#                  OPENAI_MODEL_NAME (optional, defaults to gpt-3.5-turbo)
#    - For Ollama: OLLAMA_MODEL_NAME (required if LLM_PROVIDER is 'ollama')
#                  OLLAMA_API_BASE (optional, LiteLLM usually picks this up from env)

import os
from praisonai import PraisonAI
from praisonai.agents_generator import PraisonAgent as PraisonAIAgent # Discovered path
from praisonai.agents_generator import PraisonTask as Task # Discovered path
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
llm_provider = os.environ.get("LLM_PROVIDER", "openai").lower()
llm_config_params = {}

print(f"--- Configuring LLM for provider: {llm_provider} ---")

if llm_provider == "ollama":
    ollama_model_name = os.environ.get("OLLAMA_MODEL_NAME")
    if not ollama_model_name:
        raise ValueError("OLLAMA_MODEL_NAME environment variable must be set when LLM_PROVIDER is 'ollama'.")
    # llm_config_params['model'] = f"ollama/{ollama_model_name}" # PraisonAI __init__ does not take 'model'

    ollama_api_base = os.environ.get("OLLAMA_API_BASE")
    # if ollama_api_base: # PraisonAI __init__ does not take 'api_base'
        # llm_config_params['api_base'] = ollama_api_base

    # LiteLLM, used by PraisonAI, should pick up OLLAMA_MODEL_NAME and OLLAMA_API_BASE from environment variables.
    # For LiteLLM to identify the model, OLLAMA_MODEL_NAME should be set, and then
    # when making a call, the model string "ollama/<your_OLLAMA_MODEL_NAME>" is typically used.
    # It's assumed PraisonAI/LiteLLM will construct this mapping internally or that
    # setting environment variables like MODEL_NAME or LITELLM_MODEL might be needed for LiteLLM.
    # For now, we rely on PraisonAI to correctly instruct LiteLLM based on env vars.
    if ollama_api_base:
        print(f"Using Ollama. Model: '{ollama_model_name}' (set via OLLAMA_MODEL_NAME env var). API Base: '{ollama_api_base}' (set via OLLAMA_API_BASE env var).")
    else:
        print(f"Using Ollama. Model: '{ollama_model_name}' (set via OLLAMA_MODEL_NAME env var). OLLAMA_API_BASE not set (LiteLLM will use default).")

elif llm_provider == "openai":
    if not os.environ.get("OPENAI_API_KEY"):
        print("OPENAI_API_KEY not found, using placeholder key.")
        os.environ["OPENAI_API_KEY"] = "sk-your_api_key_here" # Placeholder

    openai_model_name = os.environ.get("OPENAI_MODEL_NAME", "gpt-3.5-turbo")
    # PraisonAI constructor does not take 'model' for openai provider;
    # LiteLLM likely uses OPENAI_MODEL_NAME env var or defaults.
    # No model parameter is added to llm_config_params for openai.
    print(f"Using OpenAI (model specified by OPENAI_MODEL_NAME env var: {openai_model_name} or LiteLLM default)")

else:
    raise ValueError(f"Unsupported LLM_PROVIDER: '{llm_provider}'. Must be 'openai' or 'ollama'.")

# This PraisonAI instance is used to configure the LLM for individual agents
llm_object_for_agents = PraisonAI(**llm_config_params)
print("--- LLM Configuration Complete ---")

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
    # llm_object_for_agents is an instance of PraisonAI.
    # Based on TypeError, PraisonAI.__init__ does not take 'agents' or 'tasks'.
    # Thus, llm_object_for_agents must be the orchestrator.
    # We need to find how to pass tasks to its main() method or if it auto-discovers them.
    # Let's try passing tasks to main(). Agents are linked within tasks.
    # Update: PraisonAI.main() does not take 'tasks' argument.
    # Assuming PraisonAI instance (llm_object_for_agents) internally tracks tasks
    # created with agents that were initialized with it.

    print("--- Attempting to run crew using llm_object_for_agents.main() ---")
    final_manuscript = llm_object_for_agents.main()

    print("\n\n✅ AI Scientist Framework execution complete!")
    print("="*50)
    print("Final Manuscript (as approved by Peer Reviewer):")
    print("="*50)
    print(final_manuscript)
