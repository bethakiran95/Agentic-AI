import base64
import json
import os
import re
import sqlite3
from typing import Optional

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

from reviews_api import get_product_rating

load_dotenv()

DB_PATH = os.path.join(os.path.dirname(__file__), "store.db") # Path to the SQLite database file : 10_project_shopping_agent/store.db
PREFERENCE_NAMES = {"organic_only", "max_price", "minimum_rating"} # 

llm = ChatGroq(model="qwen/qwen3.8-27b", temperature=0)
vision_llm = ChatGoogleGenerativeAI(model="gemini-3.6-flash")


def initialize_preferences_table() -> None:
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS user_preferences (
            name TEXT PRIMARY KEY,
            value TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()


initialize_preferences_table()


# ---------------------------------------------------------------------------
# Tools
# ---------------------------------------------------------------------------

@tool
def search_products(query: str, max_price: Optional[float] = None, is_organic: Optional[bool] = None) -> str:
    """
    Search the product database by keyword (matched against name, description, and category).
    Optionally filter by maximum price and/or organic status.
    Returns a JSON array of matching products, each with: id, name, category, price,
    description, is_organic.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    sql = "SELECT id, name, category, price, description, is_organic FROM products WHERE 1=1"
    params: list = []

    if query:
        sql += " AND (name LIKE ? OR description LIKE ? OR category LIKE ?)"
        like = f"%{query}%"
        params.extend([like, like, like])

    if max_price is not None:
        sql += " AND price <= ?"
        params.append(max_price)

    if is_organic is not None:
        sql += " AND is_organic = ?"
        params.append(1 if is_organic else 0)

    cursor.execute(sql, params)
    rows = cursor.fetchall()
    conn.close()

    products = [
        {
            "id":          row[0],
            "name":        row[1],
            "category":    row[2],
            "price":       row[3],
            "description": row[4],
            "is_organic":  bool(row[5]),
        }
        for row in rows
    ]
    return json.dumps(products)


@tool
def get_rating(product_id: int) -> str:
    """
    Get the average customer rating and total review count for a product by its ID.
    Returns a JSON object with: product_id, average_rating, review_count.
    """
    result = get_product_rating(product_id)
    return json.dumps(result)


@tool
def checkout(product_id: int) -> str:
    """
    Place an order for the given product ID. Saves the order to the database and returns
    a confirmation message with the order ID, product name, and price.
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT name, price FROM products WHERE id = ?", (product_id,))
    row = cursor.fetchone()

    if not row:
        conn.close()
        return f"Error: product with ID {product_id} not found."

    name, price = row
    cursor.execute(
        "INSERT INTO orders (product_id, product_name, price) VALUES (?, ?, ?)",
        (product_id, name, price),
    )
    order_id = cursor.lastrowid
    conn.commit()
    conn.close()

    return (
        f"Order #{order_id} confirmed! '{name}' has been successfully ordered for ${price:.2f}. "
        f"Your order will arrive in 3-5 business days. Thank you for shopping with us!"
    )


@tool
def describe_product_image(image_path: str) -> str:
    """
    Analyze a product image and return its key attributes as a JSON object.
    Use this when the user uploads a photo of a product they are interested in.
    The returned attributes can be used directly with search_products.
    """
    with open(image_path, "rb") as f:
        image_data = base64.b64encode(f.read()).decode()

    ext = os.path.splitext(image_path)[1].lower().lstrip(".")
    mime = "image/jpeg" if ext in ("jpg", "jpeg") else f"image/{ext}"

    message = HumanMessage(content=[
        {
            "type": "image_url",
            "image_url": {"url": f"data:{mime};base64,{image_data}"},
        },
        {
            "type": "text",
            "text": (
                "Look at this product image and extract its key attributes. "
                "Return ONLY a JSON object with these fields:\n"
                "- product_type: what kind of product it is (e.g. honey, olive oil, almonds)\n"
                "- search_query: a short keyword to search for it (e.g. 'honey', 'olive oil')\n"
                "- is_organic: true if the label says organic, false if not, null if unclear\n"
                "- description: one sentence describing the product"
            ),
        },
    ])

    response = vision_llm.invoke([message])
    if isinstance(response.content, str):
        return response.content

    return "".join(
        block.get("text", "")
        for block in response.content
        if isinstance(block, dict) and block.get("type") == "text"
    )


@tool # allows user to ask What have I ordered before?
def get_order_history() -> str:
    """Return a summary of products previously ordered by the user."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT product_name, price, COUNT(*) AS quantity
        FROM orders
        GROUP BY product_name, price
        ORDER BY MAX(id) DESC
        """
    )
    rows = cursor.fetchall()
    conn.close()

    return json.dumps([
        {"product_name": row[0], "price": row[1], "quantity": row[2]}
        for row in rows
    ])

@tool
def save_preference(name: str, value: str) -> str:
    """Save a shopping preference for future conversations."""
    if name not in PREFERENCE_NAMES:
        return f"Unsupported preference '{name}'. Use one of: {', '.join(sorted(PREFERENCE_NAMES))}."

    normalized_value = value.strip().lower()
    if name == "organic_only":
        if normalized_value not in {"true", "false"}:
            return "organic_only must be true or false."
    else:
        try:
            numeric_value = float(normalized_value)
        except ValueError:
            return f"{name} must be a number."
        if numeric_value < 0:
            return f"{name} must not be negative."
        normalized_value = str(numeric_value)

    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        """
        INSERT INTO user_preferences (name, value)
        VALUES (?, ?)
        ON CONFLICT(name) DO UPDATE SET value = excluded.value
        """,
        (name, normalized_value),
    )
    conn.commit()
    conn.close()
    return f"Saved preference: {name}={normalized_value}."

@tool
def get_preferences() -> str:
    """Return all saved shopping preferences."""
    conn = sqlite3.connect(DB_PATH)
    rows = conn.execute(
        "SELECT name, value FROM user_preferences ORDER BY name"
    ).fetchall()
    conn.close()
    return json.dumps({name: value for name, value in rows})

# # ---------------------------------------------------------------------------
# # Agent
# # ---------------------------------------------------------------------------

agent = create_agent(
    tools=[
        search_products,
        get_rating,
        checkout,
        describe_product_image,
        get_order_history,
        save_preference,
        get_preferences,
    ],
    model=llm,
    system_prompt=(
        "You are a helpful shopping assistant. Follow these rules strictly.\n\n"
        "IMAGE SEARCH — when the user provides an image path:\n"
        "1. Call describe_product_image with the path to identify the product.\n"
        "2. Use the returned search_query and is_organic to call search_products.\n"
        "3. Continue with the BROWSING flow from step 2 onwards.\n\n"
        "MEMORY AND PERSONALIZATION:\n"
        "1. When the user asks what they ordered before, their order history, or similar, "
        "call get_order_history and summarize the result in plain English.\n"
        "2. When the user states a lasting preference, call save_preference. Supported names "
        "are organic_only, max_price, and minimum_rating.\n"
        "3. Before every product search, call get_preferences and apply saved preferences. "
        "Values explicitly stated in the current request override saved preferences.\n"
        "4. When the user asks about saved preferences, call get_preferences and summarize them.\n\n"
        "BROWSING — when the user describes what they want to buy:\n"
        "1. Call search_products to find matching items (apply any price/organic filters given).\n"
        "2. For each candidate, call get_rating to retrieve its average rating.\n"
        "3. Filter by the user's minimum rating if specified.\n"
        "4. Present qualifying products as a numbered list. For each item use this exact format "
        "   (plain text, no backticks, no code blocks, no bold, no italic):\n\n"
        "   #<number>. <name> (ID:<product_id>) — $<price> ★<rating> — <organic or non-organic>\n\n"
        "   Add a blank line between each product entry for readability. "
        "   Always include (ID:X) so you can reference it later.\n"
        "5. If only one product qualifies, still show it in the list and ask: "
        "   'Would you like to order it? Just say yes or give me the number.'\n"
        "6. Do NOT call checkout at this stage.\n\n"
        "ORDERING — when the user confirms they want to buy (e.g. 'yes', 'sure', 'go ahead', "
        "'order number 2', 'the first one', 'get me #3'):\n"
        "1. Look at your previous message to find the (ID:X) for the chosen product "
        "   (if only one was listed and the user says 'yes', use that product's ID).\n"
        "2. Call checkout with that product_id (the number from (ID:X)).\n"
        "3. Confirm the order to the user in plain text.\n\n"
        "Never place an order unless the user explicitly confirms. "
        "Never guess a product_id — always take it from the (ID:X) in your own previous message."
    ),
)

if __name__ == "__main__":
    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": (
                        "I want to buy organic honey with 4.5+ rating and less than $20 price."
                    ),
                }
            ]
        }
    )
    print(result["messages"][-1].content)

# if __name__ == "__main__":
#     result = search_products("honey", max_price=20, is_organic=True)
#     print(result)

SHOPPING_TERMS = {
    "buy", "bought", "checkout", "food", "history", "honey", "item",
    "organic", "order", "ordered", "preference", "price", "product",
    "purchase", "rating", "shop", "shopping", "store",
}

ORDER_CONFIRMATIONS = {
    "yes", "sure", "go ahead", "order it", "buy it", "checkout",
}


def is_shopping_related(message: str, allow_confirmation: bool = False) -> bool:
    """Return whether a message belongs to the shopping assistant's domain."""
    normalized = " ".join(re.findall(r"[a-z0-9]+", message.lower()))
    words = set(normalized.split())
    if words & SHOPPING_TERMS:
        return True

    return allow_confirmation and (
        normalized in ORDER_CONFIRMATIONS
        or bool(re.fullmatch(r"(?:number\s*)?#?\d+", normalized))
    )