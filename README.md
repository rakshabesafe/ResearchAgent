# AI Scientist Framework

## Project Overview
A Python application simulating an autonomous research agent using PraisonAI. Aims for a closed-loop system for iterative research and knowledge base construction.

## Current Features
*   Modular: Agents, tools, workflows in separate modules.
*   Configurable LLM: OpenAI and Ollama support.
*   Sequential Tasks: Demonstrates a research pipeline.
*   Mock Tools: Simulates research actions and evaluations.

## Planned Features
*   Full Closed-Loop Operation.
*   Enhanced Self-Evaluation.
*   Dynamic Knowledge Base.

## Project Structure
- `aiscientist.py`: Main script.
- `agents/`: Agent class definitions.
- `tools/`: `ScientificTools` class.
- `workflows/`: Task grouping classes.
- `mock_knowledge_base.jsonl`: Mock KB file.

## Setup and Installation
1.  **Prerequisites:** Python 3.8+, Git. (Optional: Ollama).
2.  **Clone:** `git clone <repository_url> && cd <repository_directory>`
3.  **Install:** `pip install praisonai litellm`
4.  **LLM Configuration (Environment Variables):**
    *   `LLM_PROVIDER`: `"openai"` (default) or `"ollama"`.
    *   **OpenAI:** `OPENAI_API_KEY`, `OPENAI_MODEL_NAME` (optional, e.g., `"gpt-3.5-turbo"`).
    *   **Ollama:** Install Ollama ([Ollama Download](https://ollama.com/download)), pull model (e.g., `ollama pull llama3`). Set `OLLAMA_MODEL_NAME` (e.g., `"llama3"`), `OLLAMA_API_BASE` (optional).

## How to Run
```bash
python aiscientist.py
```
Outputs mock tool actions and a final mock manuscript.
