import praisonai
import inspect

print("--- dir(praisonai) ---")
print(dir(praisonai))

# Attempt to find PraisonAIAgent-like and Task-like classes/modules
agent_candidates = []
task_candidates = []

# Inspect top-level attributes of praisonai
for name, obj in inspect.getmembers(praisonai):
    if 'agent' in name.lower(): # Case-insensitive check for 'agent' in attribute name
        agent_candidates.append(f"praisonai.{name}")
    if 'task' in name.lower(): # Case-insensitive check for 'task' in attribute name
        task_candidates.append(f"praisonai.{name}")

    if inspect.ismodule(obj):
        print(f"--- dir(praisonai.{name}) ---")
        try:
            print(dir(obj))
            for sub_name, sub_obj in inspect.getmembers(obj):
                # Check attributes of the submodule
                if 'agent' in sub_name.lower():
                    agent_candidates.append(f"praisonai.{name}.{sub_name}")
                if 'task' in sub_name.lower():
                    task_candidates.append(f"praisonai.{name}.{sub_name}")
                # If the submodule attribute is itself a module, recurse (optional, keep it simple for now)
        except ImportError: # Catch ImportError if a submodule is not installed/available
            print(f"Could not dir(praisonai.{name}) or one of its imports is missing.")
        except Exception as e:
            print(f"Error inspecting praisonai.{name}: {e}")

print("--- Agent Candidates based on name inspection ---")
# Filter out private/special members from candidates for clarity
agent_candidates = sorted(list(set(c for c in agent_candidates if not c.split('.')[-1].startswith('_'))))
print(agent_candidates)

print("--- Task Candidates based on name inspection ---")
task_candidates = sorted(list(set(c for c in task_candidates if not c.split('.')[-1].startswith('_'))))
print(task_candidates)

print("--- Direct Import Attempts ---")
try:
    from praisonai import PraisonAIAgent
    print("Successfully imported PraisonAIAgent from praisonai")
except ImportError as e:
    print(f"Failed to import PraisonAIAgent from praisonai: {e}")

try:
    from praisonai import Task
    print("Successfully imported Task from praisonai: {e}")
except ImportError as e:
    print(f"Failed to import Task from praisonai: {e}")

try:
    from praisonai.main import PraisonAIAgent, Task
    print("Successfully imported PraisonAIAgent and Task from praisonai.main")
    # Add these as strong candidates if successful
    agent_candidates.append("praisonai.main.PraisonAIAgent")
    task_candidates.append("praisonai.main.Task")
except ImportError as e:
    print(f"Failed to import PraisonAIAgent and Task from praisonai.main: {e}")

try:
    from praisonai.agents import Agent # Common naming
    print("Successfully imported Agent from praisonai.agents")
    agent_candidates.append("praisonai.agents.Agent (as PraisonAIAgent?)")
except ImportError as e:
    print(f"Failed to import Agent from praisonai.agents: {e}")

try:
    from praisonai.tasks import Task # Common naming
    print("Successfully imported Task from praisonai.tasks")
    task_candidates.append("praisonai.tasks.Task")
except ImportError as e:
    print(f"Failed to import Task from praisonai.tasks: {e}")

# Check praisonai.PraisonAI as it was used before
try:
    from praisonai import PraisonAI
    print("Successfully imported PraisonAI from praisonai")
    if hasattr(PraisonAI, 'PraisonAIAgent'):
        print("PraisonAI class has attribute PraisonAIAgent")
        agent_candidates.append("PraisonAI.PraisonAIAgent (attribute)")
    if hasattr(PraisonAI, 'Task'):
        print("PraisonAI class has attribute Task")
        task_candidates.append("PraisonAI.Task (attribute)")
except ImportError as e:
    print(f"Failed to import PraisonAI from praisonai: {e}")

print("--- Final Agent Candidates ---")
print(sorted(list(set(agent_candidates))))
print("--- Final Task Candidates ---")
print(sorted(list(set(task_candidates))))
