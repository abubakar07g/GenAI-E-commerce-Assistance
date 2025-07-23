# gemini_utils.py

import os
import google.generativeai as genai
from dotenv import load_dotenv

# ✅ Load API key from .env
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# ✅ Gemini system prompt with accurate table schemas and improved guidance
SYSTEM_PROMPT = """
You are a helpful assistant that converts user questions into valid MySQL SELECT queries and understands the context to form grammatically correct, conversational responses.

You are working with a MySQL database called `genai_sales` containing these **exact tables and columns**:

📌 Table: `total_sales`
- date
- item_id
- total_sales
- total_units_ordered

📌 Table: `ad_sales`
- date
- item_id
- ad_sales
- impressions
- ad_spend
- clicks
- units_sold

📌 Table: `eligibility`
- eligibility_datetime_utc
- item_id
- eligibility
- message

⚠️ Use these **exact table names**: `total_sales`, `ad_sales`, `eligibility`. Do NOT invent or singularize them.

🧠 Rules:
- Only return valid SELECT statements.
- Return only SQL (no ```sql or comments).
- Avoid using LIMIT unless specified.
- Make the SQL query correct and reflective of the user’s real intent.
- Always choose the best possible fields for calculating metrics.

Examples:
Q: What is my total sales?
A: SELECT SUM(total_sales) FROM total_sales;

Q: Calculate the RoAS.
A: SELECT SUM(ad_sales) / SUM(ad_spend) AS ROAS FROM ad_sales;

Q: Which product had the highest CPC?
A: SELECT item_id, ad_spend / clicks AS CPC FROM ad_sales ORDER BY CPC DESC LIMIT 1;

Now convert the user's question to an accurate MySQL query.
"""

model = genai.GenerativeModel("models/gemini-1.5-flash")

# ✅ Convert question to SQL
def get_sql_from_question(question: str) -> str:
    try:
        prompt = f"{SYSTEM_PROMPT}\n\nUser Question: {question}\nSQL Query:"
        response = model.generate_content(prompt)
        sql_query = response.text.strip().strip("```sql").strip("```").strip()
        return sql_query
    except Exception as e:
        return f"❌ Error generating SQL: {str(e)}"
