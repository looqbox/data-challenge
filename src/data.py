import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

from src.db_config import DB_CONFIG


def get_engine():
    required_fields = ["user", "password", "host", "database"]
    missing_fields = [field for field in required_fields if not DB_CONFIG.get(field)]

    if missing_fields:
        raise ValueError(
            "Campos ausentes na configuracao do banco: "
            + ", ".join(missing_fields)
        )

    connection_url = URL.create(
        drivername="mysql+pymysql",
        username=DB_CONFIG["user"],
        password=DB_CONFIG["password"],
        host=DB_CONFIG["host"],
        database=DB_CONFIG["database"],
    )

    return create_engine(connection_url)


def read_query(query, engine=None):
    if engine is None:
        engine = get_engine()

    return pd.read_sql(query, engine)
