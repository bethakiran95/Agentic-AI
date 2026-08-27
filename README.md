# Agentic AI Crash Course

A hands-on crash course exploring agentic AI concepts using [LangChain](https://python.langchain.com/), Google Gemini/Gemma models, Groq, and vector search with Chroma.

## Project Structure

```
1_simple_llm_calling/     # Basics of calling an LLM via LangChain (system/human messages)
2_health_analysis/        # Example: analyzing a blood work report with an LLM
src/agentic_ai_tutorial/  # Shared Python package for the project
```

### Notebooks

- [call_llm.ipynb](1_simple_llm_calling/call_llm.ipynb) — Introductory examples of invoking a chat model directly and with a system/human message pair.
- [blood_work_analysis.ipynb](2_health_analysis/blood_work_analysis.ipynb) — Loads a sample [blood_work.txt](2_health_analysis/blood_work.txt) report and analyzes it with an LLM.

## Requirements

- Python >= 3.14
- [uv](https://docs.astral.sh/uv/) (recommended) for dependency management

## Setup

1. Clone the repository and open it in VS Code.
2. Create a `.env` file in the project root with your API keys, e.g.:

   ```
   GOOGLE_API_KEY=your-google-api-key
   GROQ_API_KEY=your-groq-api-key
   ```

3. Install dependencies:

   ```bash
   uv sync
   ```

4. Activate the virtual environment:

   ```bash
   source .venv/Scripts/activate   # Windows (Git Bash)
   # or
   .venv\Scripts\Activate.ps1      # Windows (PowerShell)
   ```

5. Open the notebooks in VS Code and select the `.venv` kernel to run the cells.

## Key Dependencies

- `langchain`, `langchain-core`, `langchain-community`, `langchain-text-splitters`
- `langchain-google-genai` — Google Gemini/Gemma chat models
- `langchain-groq` — Groq-hosted models
- `langchain-chroma`, `chromadb`, `sentence-transformers` — vector storage & embeddings
- `streamlit` — for building simple UIs
- `pandas`, `pypdf`, `fpdf2`, `pillow` — data and document utilities
