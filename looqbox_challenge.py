import warnings
warnings.filterwarnings(
    "ignore",
    message="pandas only supports SQLAlchemy connectable*",
)

from cases.sql_test import execute_sql_test
from cases.case1 import retrieve_data
from cases.case2 import execute as run_case2
from cases.case3 import execute as run_case3
from utils.generate_report import build_pdf


def main():
    print("\n========== LOOQBOX CHALLENGE ==========")

    # ── Execução dos cases ───────────────────
    sql_test_result = execute_sql_test()

    case1_result = retrieve_data(
        product_code=1,
        date=["2019-01-01", "2019-01-31"],
    )

    case2_result = run_case2()

    case3_result = run_case3()

    # ── Geração do PDF ───────────────────────
    build_pdf(
        sql_test_result=sql_test_result,
        case1_result=case1_result,
        case2_result=case2_result,
        case3_result=case3_result,
        output="outputs/looqbox_report.pdf",
        logo_path="logo.png",          # raiz do projeto
    )

    print("\n✅ Execução finalizada.")


if __name__ == "__main__":
    main()