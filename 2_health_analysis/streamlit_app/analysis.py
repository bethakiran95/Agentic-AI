"""Core analysis logic: calling the LLM stages and parsing the response."""

from prompts import DIET_PROMPT_TEMPLATE, EXTRACTION_PROMPT_TEMPLATE


def extract_blood_values(llm, blood_report: str) -> str:
    """Stage 1: extract and flag abnormal values from the raw report."""
    prompt = EXTRACTION_PROMPT_TEMPLATE.format(blood_report=blood_report)
    response = llm.invoke(prompt)
    return response.text


def generate_diet_plan(llm, extracted_values: str) -> str:
    """Stage 2: produce a health summary and Indian diet plan."""
    prompt = DIET_PROMPT_TEMPLATE.format(extracted_values=extracted_values)
    response = llm.invoke(prompt)
    return response.text


def split_response(full_response: str) -> tuple[str, str]:
    """Split the stage 2 response into (health_summary, diet_plan) sections."""
    if "SECTION 2" in full_response:
        parts = full_response.split("SECTION 2")
        health_summary = (
            parts[0].replace("SECTION 1 - HEALTH SUMMARY:", "").replace("SECTION 1", "").strip()
        )
        diet_plan = (
            ("SECTION 2" + parts[1])
            .replace("SECTION 2 - INDIAN DIET PLAN:", "")
            .replace("SECTION 2", "")
            .strip()
        )
        return health_summary, diet_plan

    return full_response, ""
