import os

import mysql.connector
import pandas as pd
from dotenv import load_dotenv

load_dotenv()


def _get_connection():
    return mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        port=int(os.environ.get("DB_PORT", 3306)),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME"),
    )


def load_movies() -> pd.DataFrame:
    conn = _get_connection()
    try:
        return pd.read_sql_query("SELECT * FROM IMDB_movies", conn)
    finally:
        conn.close()
