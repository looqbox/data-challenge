"""Case 2: calculate and visualize average ticket by store."""

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from database import create_database_engine


QUERY_STORES = """
SELECT
      STORE_CODE,
      STORE_NAME,
      START_DATE,
      END_DATE,
      BUSINESS_NAME,
      BUSINESS_CODE
FROM data_store_cad
"""

QUERY_SALES = """
SELECT
        STORE_CODE,
        DATE,
        SALES_VALUE,
        SALES_QTY
FROM data_store_sales
WHERE DATE BETWEEN '2019-01-01' AND '2019-12-31'
"""

PROJECT_ROOT = Path(__file__).resolve().parents[1]
TABLE_DIR = PROJECT_ROOT / "outputs" / "tables"
CHART_DIR = PROJECT_ROOT / "outputs" / "charts"


def build_ticket_table() -> pd.DataFrame:
    """Use the supplied queries unchanged and filter the requested period in Pandas."""
    engine = create_database_engine()
    stores = pd.read_sql_query(QUERY_STORES, engine)
    sales = pd.read_sql_query(QUERY_SALES, engine)
    engine.dispose()

    sales["DATE"] = pd.to_datetime(sales["DATE"])
    period_sales = sales.loc[
        sales["DATE"].between("2019-10-01", "2019-12-31", inclusive="both")
    ].copy()

    joined = period_sales.merge(stores, on="STORE_CODE", how="inner", validate="many_to_one")
    grouped = (
        joined.groupby(["STORE_CODE", "STORE_NAME", "BUSINESS_NAME"], as_index=False)
        .agg(SALES_VALUE=("SALES_VALUE", "sum"), SALES_QTY=("SALES_QTY", "sum"))
    )
    grouped = grouped.loc[grouped["SALES_QTY"] != 0].copy()
    grouped["TM"] = grouped["SALES_VALUE"] / grouped["SALES_QTY"]

    return (
        grouped.rename(columns={"STORE_NAME": "Loja", "BUSINESS_NAME": "Categoria"})
        .loc[:, ["Loja", "Categoria", "TM"]]
        .sort_values("Loja")
        .reset_index(drop=True)
    )


def main() -> None:
    TABLE_DIR.mkdir(parents=True, exist_ok=True)
    CHART_DIR.mkdir(parents=True, exist_ok=True)
    tickets = build_ticket_table()
    tickets.to_csv(TABLE_DIR / "case_02_ticket_by_store.csv", index=False, float_format="%.2f")

    plot_data = tickets.sort_values("TM")
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.barh(plot_data["Loja"], plot_data["TM"], color="#2563EB")
    ax.set(title="Ticket médio por loja — out. a dez. de 2019", xlabel="Ticket médio (TM)", ylabel="")
    ax.grid(axis="x", alpha=0.25)
    fig.tight_layout()
    fig.savefig(CHART_DIR / "case_02_ticket_by_store.png", dpi=180, bbox_inches="tight")
    plt.close(fig)
    print(f"Case 2 complete: {len(tickets)} stores")


if __name__ == "__main__":
    main()
