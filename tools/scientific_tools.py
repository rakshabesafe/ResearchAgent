import json
import random # For execute_python_code simulation
import os # For query_knowledge_base

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
    def execute_python_code(code: str) -> dict:
        """
        Simulates executing Python code in a sandboxed environment.
        Returns a mock result of the execution, including success/failure.
        """
        print(f"\n MOCK TOOL: Executing Python code in a sandbox...")
        # print("--- CODE ---\n" + code + "\n------------")
        # In a real implementation, NEVER use exec() on LLM-generated code
        # without extreme sandboxing and security measures.

        # Simulate potential failure
        if "error" in code.lower() or random.random() < 0.1: # 10% chance of mock error
            return {"success": False, "output": None, "error": "SyntaxError: Invalid syntax on mock line 5 (simulated)"}

        return {"success": True, "output": "Execution successful. Data saved to 'results.csv'.\nColumns: 'molecule_id', 'binding_affinity', 'toxicity_score'", "error": None}

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

    # --- New Mock Tools for Closed-Loop System ---

    @staticmethod
    def evaluate_hypothesis_clarity(hypothesis: str) -> dict:
        """
        Simulates evaluating the clarity and testability of a hypothesis.
        """
        print(f"\n MOCK TOOL: Evaluating hypothesis clarity for: '{hypothesis[:50]}...'")
        # Simulate some basic checks
        is_clear = "complex" not in hypothesis.lower()
        is_testable = "evaluate" in hypothesis.lower() or "test" in hypothesis.lower()
        score = (0.7 if is_clear else 0.3) + (0.3 if is_testable else 0.0)

        feedback_msg = "Mock: Hypothesis seems "
        feedback_parts = []
        if is_clear:
            feedback_parts.append("clear")
        else:
            feedback_parts.append("a bit unclear")
        if is_testable:
            feedback_parts.append("testable")
        else:
            feedback_parts.append("hard to test")
        feedback_msg += " and ".join(feedback_parts) + "."

        return {
            "score": round(score, 2),
            "feedback": feedback_msg,
            "is_clear": is_clear,
            "is_testable": is_testable,
            "proceed": is_clear and is_testable # Only proceed if both are true
        }

    @staticmethod
    def evaluate_experimental_design_soundness(design_description: str, hypothesis: str) -> dict:
        """
        Simulates evaluating the soundness of an experimental design.
        """
        print(f"\n MOCK TOOL: Evaluating experimental design soundness for design: '{design_description[:50]}...' related to hypothesis: '{hypothesis[:50]}...'")
        # Simulate basic checks
        aligns = "hypothesis" in design_description.lower() or "test" in design_description.lower()
        is_sound = "steps" in design_description.lower() and "control" in design_description.lower()
        score = (0.5 if aligns else 0.2) + (0.5 if is_sound else 0.2)

        feedback_msg = "Mock: Design "
        if aligns:
            feedback_msg += "aligns with hypothesis. "
        else:
            feedback_msg += "may not fully align with hypothesis. "
        if is_sound:
            feedback_msg += "Seems sound."
        else:
            feedback_msg += "Could be more robust (e.g., ensure clear steps and controls)."

        return {
            "score": round(score,2),
            "feedback": feedback_msg,
            "aligns_with_hypothesis": aligns,
            "is_sound": is_sound,
            "proceed": aligns and is_sound
        }

    @staticmethod
    def analyze_code_for_errors(code: str, error_message: str = None) -> dict:
        """
        Simulates analyzing code for errors, optionally with a reported error message.
        """
        if error_message:
            print(f"\n MOCK TOOL: Analyzing code for errors, focusing on reported error: {error_message}")
            # Simulate more targeted analysis
            if "syntax" in error_message.lower():
                 return {"diagnosis": "Mock: Likely a syntax error based on report.", "suggested_fix": "Mock: Double-check syntax, colons, parentheses, and indentation around the reported error location.", "confidence": 0.85}
            return {"diagnosis": "Mock: Error type unclear from message.", "suggested_fix": "Mock: General debugging steps: print statements, simplify code.", "confidence": 0.4}

        print(f"\n MOCK TOOL: Analyzing code for potential errors: '{code[:100]}...'")
        # Simulate generic analysis
        if "import non_existent_module" in code:
            return {"diagnosis": "Mock: Identified an import error.", "suggested_fix": "Mock: Ensure 'non_existent_module' is installed and correctly named.", "confidence": 0.9}
        if "print(variable_not_defined)" in code:
            return {"diagnosis": "Mock: Identified a NameError.", "suggested_fix": "Mock: Ensure 'variable_not_defined' is defined before use.", "confidence": 0.8}

        return {"diagnosis": "Mock: No obvious errors found in this simple scan.", "suggested_fix": "Mock: If issues persist, try manual debugging or more detailed static analysis.", "confidence": 0.6}

    @staticmethod
    def compare_results_to_hypothesis(results_summary: str, hypothesis: str) -> dict:
        """
        Simulates comparing experimental results to the initial hypothesis.
        """
        print(f"\n MOCK TOOL: Comparing results '{results_summary[:50]}...' to hypothesis '{hypothesis[:50]}...'")
        # Simple mock logic
        conclusion = "supports"
        confidence = 0.75
        summary = f"Mock: Results ('{results_summary}') appear to support the hypothesis ('{hypothesis}')."

        if "not" in results_summary.lower() or "fail" in results_summary.lower():
            conclusion = "contradicts"
            confidence = 0.70
            summary = f"Mock: Results ('{results_summary}') seem to contradict the hypothesis ('{hypothesis}')."
        elif "inconclusive" in results_summary.lower():
            conclusion = "inconclusive"
            confidence = 0.5
            summary = f"Mock: Results ('{results_summary}') are inconclusive regarding the hypothesis ('{hypothesis}')."

        return {"conclusion": conclusion, "confidence": confidence, "summary": summary}

    @staticmethod
    def update_knowledge_base(entry: dict) -> bool:
        """
        Simulates updating a knowledge base with a new entry.
        """
        print(f"\n MOCK TOOL: Updating knowledge base with entry: {str(entry)[:100]}...")
        try:
            with open("mock_knowledge_base.jsonl", "a") as f:
                f.write(json.dumps(entry) + '\n')
            return True
        except Exception as e:
            print(f" MOCK TOOL ERROR: Failed to write to mock_knowledge_base.jsonl: {e}")
            return False

    @staticmethod
    def query_knowledge_base(query: str) -> list[dict]:
        """
        Simulates querying a knowledge base.
        """
        print(f"\n MOCK TOOL: Querying knowledge base for: '{query}'")
        # Simulate reading from the mock KB for more dynamic results if it exists
        mock_kb_path = "mock_knowledge_base.jsonl"
        found_entries = []
        try:
            if os.path.exists(mock_kb_path): # Need to import os for this
                with open(mock_kb_path, "r") as f:
                    for line in f:
                        entry = json.loads(line)
                        # Simple text matching for query simulation
                        if query.lower() in str(entry.values()).lower():
                            found_entries.append(entry)
            if found_entries:
                 return found_entries[:3] # Return up to 3 matches
        except Exception as e:
            print(f" MOCK TOOL ERROR: Failed to read or parse mock_knowledge_base.jsonl: {e}")

        # Fallback mock response
        return [{"mock_entry_id": random.randint(1, 1000), "text": f"Mock KB entry related to '{query}'. No dynamic matches found or KB empty/error."}]
