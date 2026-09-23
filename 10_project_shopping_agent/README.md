# AI Shopping Assistant

This project is a practical AI shopping assistant built with LangChain, Streamlit, Groq, Google Gemini, and SQLite. It shows how an AI agent can understand a shopping request, use tools to find products, compare ratings, remember preferences, and complete an order after user confirmation.

## What the Project Covers

- Product search by name, description, category, price, and organic status
- Customer rating lookup from a local database
- Product search using an uploaded image
- Saved shopping preferences for price, rating, and organic products
- Previous order history
- Checkout with explicit user confirmation
- Guardrails that keep the conversation focused on shopping
- A Streamlit chat interface

## How It Works

1. The user enters a shopping request or uploads a product image.
2. The agent reads saved preferences and searches the product database.
3. It retrieves ratings for matching products.
4. The assistant presents suitable products to the user.
5. An order is created only after the user confirms the purchase.

## Project Files

| File | Purpose |
| --- | --- |
| `app.py` | Provides the Streamlit chat and image-upload interface. |
| `shopping_agent.py` | Defines the AI models, tools, agent instructions, memory, and shopping guardrail. |
| `reviews_api.py` | Reads and summarizes product ratings from SQLite. |
| `store.db` | Stores products, reviews, orders, and user preferences. |
| `resources/` | Contains sample product images for testing image search. |

## Main Technologies

- Python
- LangChain
- Groq
- Google Gemini
- Streamlit
- SQLite

## Setup

Run these commands from the repository root.

```bash
python -m venv .venv
```

Activate the environment on Windows:

```powershell
.venv\Scripts\Activate.ps1
```

Install the project dependencies:

```bash
pip install -e .
```

Create a `.env` file in the repository root and add your API keys:

```env
GROQ_API_KEY=your_groq_api_key
GOOGLE_API_KEY=your_google_api_key
```

Do not commit API keys to source control.

## Run the Application

From the repository root, run:

```bash
streamlit run 10_project_shopping_agent/app.py
```

Streamlit will display the local application URL in the terminal.

## Example Requests

- `Show me organic honey under $20 with a rating above 4.5.`
- `Remember that I only want organic products.`
- `What have I ordered before?`
- Upload a product image and select **Find similar products**.
- After reviewing a result, say `Order number 1` to confirm a purchase.

## Learning Outcome

This project brings together the main ideas of agentic AI: model interaction, tool calling, database access, multimodal input, memory, guardrails, and a user-facing application. It demonstrates how these parts work together in a complete shopping workflow.