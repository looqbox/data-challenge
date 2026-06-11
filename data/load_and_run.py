import pandas as pd
from config.database import get_connection
from pathlib import Path

def load_sql(filename: str) -> str:
    sql_path = Path("data/sql") / filename

    with open(sql_path, encoding="utf-8") as sql_file:
        return sql_file.read()

def run_query(sql, params=None):
    conn = get_connection()
    return pd.read_sql(sql, conn, params=params)