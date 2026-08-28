"""LLM client setup for the Blood Work Analyzer app."""

from langchain_google_genai import ChatGoogleGenerativeAI

MODEL_NAME = "gemma-4-31b-it"


def get_llm() -> ChatGoogleGenerativeAI:
    """Create and return the chat model used for both analysis stages."""
    return ChatGoogleGenerativeAI(model=MODEL_NAME)


# --- Example: calling Google's SDK directly, without LangChain ---
#
# LangChain's `ChatGoogleGenerativeAI` above is a thin wrapper around Google's
# own `google-genai` SDK. The same call could be made without LangChain like this:
#
# from google import genai
#
# client = genai.Client()  # reads GOOGLE_API_KEY from the environment
#
# def get_llm_response(prompt: str) -> str:
#     response = client.models.generate_content(
#         model=MODEL_NAME,
#         contents=prompt,
#     )
#     return response.text
#
# Usage would then be `get_llm_response("How many moons does Jupiter have?")`
# instead of `get_llm().invoke(prompt).text`. Dropping LangChain removes the
# `langchain` / `langchain-core` / `langchain-google-genai` dependencies, but
# also loses LangChain's shared interface across providers (e.g. Groq).
