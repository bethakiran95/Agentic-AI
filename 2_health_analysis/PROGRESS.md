# Progress Log

## 1. Health / Blood Work Analysis

### Notebook prototype ([2_health_analysis/blood_work_analysis.ipynb](../2_health_analysis/blood_work_analysis.ipynb))

- Loaded a sample report from [blood_work.txt](../2_health_analysis/blood_work.txt).
- **Stage 1 — Extraction**: prompted the LLM to read the raw report and classify every test value as `HIGH` / `LOW` / `NORMAL` against the reference ranges in the text.
- **Stage 2 — Diet plan**: fed the Stage 1 output into a second prompt asking for a short health summary plus an Indian diet plan (foods to avoid / foods to eat more of).
- This validated the two-stage "extract, then reason" prompting pattern before building a UI around it.

### Streamlit app ([2_health_analysis/streamlit_app/](../2_health_analysis/streamlit_app/))

- Built a two-column Streamlit UI: paste a blood report on the left, see a health summary and diet plan rendered in scrollable boxes on the right.
- Initially implemented as a single `app.py` with the LLM client, prompts, and parsing logic all inline.
- **Refactored into modules** so the file isn't doing everything at once:
  - [`llm_client.py`](../2_health_analysis/streamlit_app/llm_client.py) — creates the `ChatGoogleGenerativeAI` instance (model name lives here).
  - [`prompts.py`](../2_health_analysis/streamlit_app/prompts.py) — the extraction and diet-plan prompt templates.
  - [`analysis.py`](../2_health_analysis/streamlit_app/analysis.py) — `extract_blood_values()`, `generate_diet_plan()`, and `split_response()` (parses the LLM's two-section reply).
  - [`app.py`](../2_health_analysis/streamlit_app/app.py) — only Streamlit UI/layout and wiring; imports the pieces above instead of inlining prompt strings and parsing logic.
- Suppressed the benign `google-genai` "Direct use of automatic function calling" warning that appears on every `.invoke()` call.

## Why modularize?

Splitting `app.py` into `llm_client.py` / `prompts.py` / `analysis.py` keeps each concern testable and reusable on its own (e.g. `analysis.py` has no Streamlit dependency, so it can be unit-tested or reused from a notebook/CLI), and keeps the UI file focused only on layout and rendering.
