"""Safely test the MySQL connection configured in a local .env file."""

import os

from dotenv import load_dotenv
from sqlalchemy import URL, create_engine, text


def build_database_url() -> URL:
    """Build a SQLAlchemy URL without exposing the password in source code."""
    load_dotenv()
    required = ("DB_HOST", "DB_PORT", "DB_USER", "DB_PASSWORD", "DB_NAME")
    missing = [name for name in required if not os.getenv(name)]
    if missing:
        raise RuntimeError(f"Missing environment variables: {', '.join(missing)}")

    return URL.create(
        drivername="mysql+pymysql",
        username=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        host=os.environ["DB_HOST"],
        port=int(os.environ["DB_PORT"]),
        database=os.environ["DB_NAME"],
    )


def main() -> None:
    engine = create_engine(build_database_url(), pool_pre_ping=True)
    with engine.connect() as connection:
        result = connection.execute(text("SELECT DATABASE() AS database_name, VERSION() AS mysql_version"))
        row = result.mappings().one()
        print(f"Connection successful. Database: {row['database_name']}; MySQL: {row['mysql_version']}")
    engine.dispose()


if __name__ == "__main__":
    main()
