import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv
import urllib.parse

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

encoded_password = urllib.parse.quote(DB_PASSWORD)

engine = create_engine(f"mysql+pymysql://{DB_USER}:{encoded_password}@{DB_HOST}/{DB_NAME}")

def fetch_table_data(table_name):
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql(query, con=engine)
    return df.to_dict(orient='records')
