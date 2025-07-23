from flask import Flask, request, jsonify
from flask_cors import CORS
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os
import logging
from gemini_utils import get_sql_from_question

# ✅ Logging setup
logging.basicConfig(level=logging.INFO)

# ✅ Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# ✅ DB Config
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
from urllib.parse import quote_plus

encoded_password = quote_plus(DB_PASSWORD)
engine = create_engine(f"mysql+pymysql://{DB_USER}:{encoded_password}@{DB_HOST}/{DB_NAME}")

# ✅ Create SQLAlchemy engine
#engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}")

# ✅ Valid table names for safety
VALID_TABLES = ["total_sales", "ad_sales", "eligibility"]

# ✅ Root route
@app.route('/')
def index():
    return "✅ GenAI E-commerce Agent is running!"

# ✅ Route: Load specific table data
@app.route('/api/data/<table_name>', methods=['GET'])
def get_table_data(table_name):
    if table_name not in VALID_TABLES:
        return jsonify({"error": "Invalid table name."}), 400
    try:
        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT * FROM {table_name}"))
            rows = [dict(row._mapping) for row in result]
        return jsonify(rows)
    except Exception as e:
        logging.error("❌ Error fetching table: %s", e)
        return jsonify({"error": str(e)}), 500

# ✅ Route: Ask Gemini + execute SQL
@app.route('/api/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json()
        question = data.get('question')

        if not question:
            return jsonify({"error": "No question provided."}), 400

        # ✅ Get SQL from Gemini
        sql_query = get_sql_from_question(question)
        logging.info("🔍 Generated SQL:\n%s", sql_query)

        # ✅ Run query
        with engine.connect() as conn:
            result = conn.execute(text(sql_query))
            rows = [dict(row._mapping) for row in result]

        return jsonify({
            "question": question,
            "sql": sql_query,
            "result": rows
        })

    except Exception as e:
        logging.error("❌ Error in /api/ask: %s", e)
        return jsonify({"error": str(e)}), 500

# ✅ Run server
if __name__ == '__main__':
    app.run(debug=True)
