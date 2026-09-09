import truststore
truststore.inject_into_ssl()

from dotenv import load_dotenv
# from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.tools import tool
from langchain.agents import create_agent
from langchain.agents.middleware import PIIMiddleware
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(model="qwen/qwen3.8-27b", temperature=0)

@tool
def get_customer_info_tool(customer_name: str) -> str:
    """
    Fetches customer information based on a given customer name.
    This is a placeholder function that simulates retrieving customer data.
    In a real implementation, this would query a database or external API.
    """
    # Simulated customer data   
    customers = {
        "Krishna": {
            "email": "krishna@example.com",
            "phone": "123-456-7890",
            "name": "Krishna",
            "loyalty_status": "Gold"
        },
        "Alice": {
            "email": "alice@example.com",
            "phone": "987-654-3210",
            "name": "Alice",
            "loyalty_status": "Silver"
        },
        "Bob": {
            "email": "bob@example.com",
            "phone": "555-555-5555",
            "name": "Bob",
            "loyalty_status": "Bronze"
        }
    }
    return customers.get(customer_name, "Customer not found.")

# ── Agent setup ───────────────────────────────────────────────────────────────

agent = create_agent(
    system_prompt="""You are a customer service assistant.
    You have access to the get_customer_info_tool which provides customer information based on the customer's name.
    When a user asks for information about a customer, use the get_customer_info_tool to retrieve the data.
    IMPORTANT RULES:
    1. Return all data fields EXACTLY as received from the tool — do NOT reformat, abbreviate, paraphrase, or restructure any field values (especially numbers and emails).
    2. Do not handle PII directly. Middleware will automatically redact/mask sensitive fields — your job is only to pass the raw values through unchanged.
    3. Return information as plain text, not JSON.
    4. Credit card numbers must always be returned in their original format with dashes e.g., XXXX-XXXX-XXXX-XXXX — never remove dashes or spaces.
    """,
    model=llm,
    tools=[get_customer_info_tool],
    middleware=[
        PIIMiddleware(
            "credit_card",
            strategy="mask",
            apply_to_tool_results=True,
        ),
        PIIMiddleware(
            "email",
            strategy="mask",
            apply_to_tool_results=True,
            apply_to_output=True,
        ),
    ]
)

# When user provides PII, it will be handled according to the strategy

result = agent.invoke({
    "messages": [{
        "role": "user",
        "content": "Give me information about customer Krishna"
    }]
})

# print(result)
print(result["messages"][-1].content)