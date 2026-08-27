"""LLM client setup for the Blood Work Analyzer app."""

from langchain_google_genai import ChatGoogleGenerativeAI

MODEL_NAME = "gemma-4-31b-it"


def get_llm() -> ChatGoogleGenerativeAI:
    """Create and return the chat model used for both analysis stages."""
    return ChatGoogleGenerativeAI(model=MODEL_NAME)
