"""Execute the three SQL questions and save their results as CSV files."""

from pathlib import Path

import pandas as pd
from sqlalchemy import text

from database import create_database_engine


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SQL_DIR = PROJECT_ROOT / "sql"
OUTPUT_DIR = PROJECT_ROOT / "outputs" / "tables"


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    engine = create_database_engine()

    for sql_path in sorted(SQL_DIR.glob("question_*.sql")):
        query = sql_path.read_text(encoding="utf-8")
        with engine.connect() as connection:
            result = pd.read_sql_query(text(query), connection)
        output_path = OUTPUT_DIR / f"{sql_path.stem}.csv"
        result.to_csv(output_path, index=False)
        print(f"{sql_path.name}: {len(result)} rows -> {output_path.name}")

    engine.dispose()


if __name__ == "__main__":
    main()
