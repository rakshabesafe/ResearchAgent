# AI Scientist Framework using PraisonAI
# This script implements the high-level design for an autonomous research agent.
# ... (rest of the header comments)

import os
import asyncio # Added for MCP and atexit
import atexit   # Added for MCP cleanup
import traceback # For more detailed error logging in MCP test

from praisonai import PraisonAI
from praisonai.agents_generator import PraisonAgent as PraisonAIAgent # Discovered path
from praisonai.agents_generator import PraisonTask as Task # Discovered path

from tools.scientific_tools import ScientificTools
from tools.mcp_integration import MCPClientManager, MCPToolWrapper # Added for MCP
# For the direct test, we might need to access the (potentially dummy) client classes
from tools.mcp_integration import streamablehttp_client as mcp_streamablehttp_client
from tools.mcp_integration import ClientSession as MCPClientSession


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

# --- MCP Setup ---
print("--- Initializing MCP Client Manager ---")
mcp_manager = MCPClientManager()

# Define a wrapper function for asyncio.run for atexit
def _run_async_cleanup():
    try:
        asyncio.run(mcp_manager.close_all_sessions())
    except RuntimeError as e:
        print(f"Error during atexit cleanup of MCP sessions: {e}")
        try:
            loop = asyncio.get_event_loop_policy().get_event_loop()
            if loop.is_closed():
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            loop.run_until_complete(mcp_manager.close_all_sessions())
        except Exception as final_e:
            print(f"Fallback MCP cleanup also failed: {final_e}")

atexit.register(_run_async_cleanup)
print("--- MCP Client Manager Initialized and Cleanup Registered ---")

MCP_TOOLS_CONFIG = [
    {
        "server_url": "http://localhost:8079/mcp",
        "tool_name": "echo_tool",
        "description": "Echoes a message using a local MCP server. Input: message (string).",
        "assign_to_agent": "ResearcherAgent"
    }
]

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

    # --- MCP Connection Test ---
    print("\n--- Testing MCP Connection Logic ---")

    async def _run_mcp_direct_test():
        echo_tool_config = None
        for config in MCP_TOOLS_CONFIG: # MCP_TOOLS_CONFIG is global
            if config["tool_name"] == "echo_tool":
                echo_tool_config = config
                break

        if not echo_tool_config:
            print("MCP Echo Tool config not found. Test cannot run.")
            return

        server_url = echo_tool_config["server_url"]
        print(f"MCP Test: Attempting to connect to MCP server at: {server_url}")

        transport_cm = None
        session = None # Renamed from 'session' in template to avoid conflict if any
        try:
            # Using imports from tools.mcp_integration which handle dummy classes if mcp not installed
            print("MCP Test: About to call mcp_streamablehttp_client...")
            transport_cm = mcp_streamablehttp_client(server_url)
            print("MCP Test: mcp_streamablehttp_client call returned. About to __aenter__ transport...")

            read_stream, write_stream, actual_transport_obj = await transport_cm.__aenter__() # actual_transport_obj was transport
            print(f"MCP Test: Transport __aenter__ completed. Streams and transport object ({type(actual_transport_obj)}) obtained.")

            print("MCP Test: About to create MCPClientSession...")
            mcp_session = MCPClientSession(read_stream, write_stream) # mcp_session was session
            print("MCP Test: MCPClientSession created. About to session.initialize()...")

            await mcp_session.initialize()
            print("MCP Test: mcp_session.initialize() completed successfully.")
            print("MCP Test: Connection and initialization successful!")

        except ImportError as ie:
            print(f"MCP Test: ImportError - mcp library might not be fully installed/available: {ie}")
        except TimeoutError:
            print("MCP Test: Caught TimeoutError during MCP connection/initialization.")
        except Exception as e:
            print(f"MCP Test: An error occurred during MCP connection/initialization: {e}")
            print(traceback.format_exc())
        finally:
            print("MCP Test: In finally block.")
            # Note: mcp_session is the ClientSession, actual_transport_obj is the transport from __aenter__
            # ClientSession itself might not be an async context manager.
            # The transport_cm is the context manager for the transport.
            if transport_cm and hasattr(transport_cm, '__aexit__'):
                try:
                    print("MCP Test: Attempting to close transport context manager...")
                    await transport_cm.__aexit__(None, None, None) # type: ignore
                    print("MCP Test: Transport context manager closed.")
                except Exception as e_trans_close:
                    print(f"MCP Test: Error closing transport context manager: {e_trans_close}")
            else:
                print("MCP Test: No transport_cm to close or it lacks __aexit__.")
            print("MCP Test: Cleanup attempted.")

    try:
        asyncio.run(_run_mcp_direct_test())
    except RuntimeError as e:
        print(f"Could not run MCP direct test with asyncio.run (possibly due to existing loop): {e}")

    print("--- MCP Connection Test Complete ---")
