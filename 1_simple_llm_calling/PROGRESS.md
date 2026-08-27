# Progress Log

This is a generative AI application built using LangChain and Google Gemini/Gemma chat models.

## Simple LLM Calling ([call_llm.ipynb](call_llm.ipynb))

- Set up `ChatGoogleGenerativeAI` from `langchain-google-genai` and loaded credentials via `.env` (`load_dotenv`).
- Basic single-turn invocation: `llm.invoke("How many moons does Jupiter have?")`.
- System + human message invocation using a `[["system", ...], ["human", ...]]` message list to constrain the response style (short one-liner).
- Compared model outputs across different models/temperatures (`gemini-3.6-flash` at `temperature=0` vs `gemini-3.5-flash` at `temperature=1`) using the same prompt to observe determinism vs creativity.
