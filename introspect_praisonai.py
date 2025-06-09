import praisonaiagents
import inspect

print("--- dir(praisonaiagents) ---")
print(dir(praisonaiagents))

# Attempt to find PraisonAIAgent-like and Task-like classes/modules
agent_candidates = []
task_candidates = []

# Inspect top-level attributes of praisonaiagents
for name, obj in inspect.getmembers(praisonaiagents):
    if 'agent' in name.lower(): # Case-insensitive check for 'agent' in attribute name
        agent_candidates.append(f"praisonaiagents.{name}")
    if 'task' in name.lower(): # Case-insensitive check for 'task' in attribute name
        task_candidates.append(f"praisonaiagents.{name}")

    if inspect.ismodule(obj):
        print(f"--- dir(praisonaiagents.{name}) ---")
        try:
            print(dir(obj))
            for sub_name, sub_obj in inspect.getmembers(obj):
                # Check attributes of the submodule
                if 'agent' in sub_name.lower():
                    agent_candidates.append(f"praisonaiagents.{name}.{sub_name}")
                if 'task' in sub_name.lower():
                    task_candidates.append(f"praisonaiagents.{name}.{sub_name}")
                # If the submodule attribute is itself a module, recurse (optional, keep it simple for now)
        except ImportError: # Catch ImportError if a submodule is not installed/available
            print(f"Could not dir(praisonaiagents.{name}) or one of its imports is missing.")
        except Exception as e:
            print(f"Error inspecting praisonaiagents.{name}: {e}")

print("--- Agent Candidates based on name inspection ---")
# Filter out private/special members from candidates for clarity
agent_candidates = sorted(list(set(c for c in agent_candidates if not c.split('.')[-1].startswith('_'))))
print(agent_candidates)

print("--- Task Candidates based on name inspection ---")
task_candidates = sorted(list(set(c for c in task_candidates if not c.split('.')[-1].startswith('_'))))
print(task_candidates)

print("--- Direct Import Attempts ---")
try:
    from praisonaiagents import Agent as PraisonAIAgent
    print("Successfully imported Agent as PraisonAIAgent from praisonaiagents")
except ImportError as e:
    print(f"Failed to import Agent as PraisonAIAgent from praisonaiagents: {e}")

try:
    from praisonaiagents import Task
    print("Successfully imported Task from praisonaiagents")
except ImportError as e:
    print(f"Failed to import Task from praisonaiagents: {e}")

# try:
#     from praisonai.main import PraisonAIAgent, Task # This structure likely changed
#     print("Successfully imported PraisonAIAgent and Task from praisonai.main")
#     # Add these as strong candidates if successful
#     agent_candidates.append("praisonai.main.PraisonAIAgent")
#     task_candidates.append("praisonai.main.Task")
# except ImportError as e:
#     print(f"Failed to import PraisonAIAgent and Task from praisonai.main: {e}")

try:
    from praisonaiagents import Agent # Common naming
    print("Successfully imported Agent from praisonaiagents")
    agent_candidates.append("praisonaiagents.Agent (as PraisonAIAgent?)")
except ImportError as e:
    print(f"Failed to import Agent from praisonaiagents: {e}")

try:
    from praisonaiagents import Task # Common naming
    print("Successfully imported Task from praisonaiagents")
    task_candidates.append("praisonaiagents.Task")
except ImportError as e:
    print(f"Failed to import Task from praisonaiagents: {e}")

# Check praisonaiagents.PraisonAIAgents (new name for PraisonAI)
try:
    from praisonaiagents import PraisonAIAgents
    print("Successfully imported PraisonAIAgents from praisonaiagents")
    # PraisonAIAgents is the new Workflow/main class, not a direct container for Agent/Task classes in the same way
    # if hasattr(PraisonAIAgents, 'Agent'): # Check for 'Agent'
    #     print("PraisonAIAgents class has attribute Agent")
    #     agent_candidates.append("PraisonAIAgents.Agent (attribute)")
    # if hasattr(PraisonAIAgents, 'Task'): # Check for 'Task'
    #     print("PraisonAIAgents class has attribute Task")
    #     task_candidates.append("PraisonAIAgents.Task (attribute)")
except ImportError as e:
    print(f"Failed to import PraisonAIAgents from praisonaiagents: {e}")

print("--- Final Agent Candidates ---")
print(sorted(list(set(agent_candidates))))
print("--- Final Task Candidates ---")
print(sorted(list(set(task_candidates))))

print("\n--- Introspecting PraisonAIAgents instance methods ---")
try:
    from praisonaiagents import PraisonAIAgents
    from praisonaiagents import Agent

    # Create dummy agents for instantiation
    dummy_agent_1 = Agent(role="Test Agent 1", goal="Test goal 1", backstory="Test backstory 1", llm="gpt-3.5-turbo")
    dummy_agent_2 = Agent(role="Test Agent 2", goal="Test goal 2", backstory="Test backstory 2", llm="gpt-3.5-turbo")

    # Minimal instantiation of PraisonAIAgents
    # Requires OPENAI_API_KEY to be set, even if 'not-needed', due to underlying LiteLLM/OpenAI client instantiation
    # The 'process' argument was seen in aiscientist.py
    praison_ai_instance = PraisonAIAgents(agents=[dummy_agent_1, dummy_agent_2], process="workflow")

    print("--- dir(PraisonAIAgents_instance) ---")
    instance_methods = [m for m in dir(praison_ai_instance) if not m.startswith('_')]
    print(instance_methods)

    # Specifically check for common kickoff methods if not obvious
    for method_name in ["run", "main", "start", "kickoff", "execute", "initiate_process", "process_tasks"]:
        if hasattr(praison_ai_instance, method_name):
            print(f"Found potential kickoff method: {method_name}")

except ImportError as e:
    print(f"Failed to import PraisonAIAgents or Agent for instance introspection: {e}")
except Exception as e:
    print(f"Error during PraisonAIAgents instance introspection: {e}")
