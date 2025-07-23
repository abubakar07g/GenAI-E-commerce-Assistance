from sqlalchemy import create_engine
import pandas as pd
import os
from dotenv import load_dotenv
import urllib.parse

# ✅ Load environment variables
load_dotenv(dotenv_path='./.env')

# ✅ Fetch DB credentials
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# ✅ Encode password
encoded_password = urllib.parse.quote(DB_PASSWORD)

# ✅ SQLAlchemy engine
engine = create_engine(f"mysql+pymysql://{DB_USER}:{encoded_password}@{DB_HOST}/{DB_NAME}")

# ✅ Mapping: CSV → Table
file_table_map = {
    "../../datasets/Product-Level Total Sales and Metrics (mapped).csv": "total_sales",
    "../../datasets/Product-Level Ad Sales and Metrics (mapped).csv": "ad_sales",
    "../../datasets/Product-Level Eligibility Table (mapped).csv": "eligibility"
}

# ✅ Upload function
def load_and_upload(csv_path, table_name):
    try:
        print(f"📥 Loading: {csv_path}")
        df = pd.read_csv(csv_path, encoding='utf-8')
        df.columns = [col.strip().replace(" ", "_").lower() for col in df.columns]
        df.to_sql(table_name, con=engine, if_exists='replace', index=False)
        print(f"✅ Uploaded to `{table_name}`\n")
    except Exception as e:
        print(f"❌ Error uploading `{table_name}`: {e}\n")

# ✅ Process each file
for path, table in file_table_map.items():
    if os.path.exists(path):
        load_and_upload(path, table)
    else:
        print(f"❌ File not found: {path}")
