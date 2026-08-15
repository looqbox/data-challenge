import pandas as pd
from sqlalchemy import create_engine

# Conexão com o banco de dados MySQL
engine = create_engine(
    "mysql+pymysql://looqbox-challenge:looq-challenge@35.199.115.174:3306/looqbox-challenge"
)

def retrieve_data(
    product_code: int,
    store_code: int,
    date: list[str]
) -> pd.DataFrame:

    # Validação dos códigos
    if not isinstance(product_code, int):
        raise TypeError("product_code deve ser um inteiro.")

    if not isinstance(store_code, int):
        raise TypeError("store_code deve ser um inteiro.")

    # Validação das datas
    if not isinstance(date, list):
        raise TypeError("date deve ser uma lista.")

    if len(date) != 2:
        raise ValueError(
            "date deve conter uma data inicial e uma data final."
        )

    try:
        start_date = pd.to_datetime(date[0])
        end_date = pd.to_datetime(date[1])
    except ValueError:
        raise ValueError(
            "As datas devem estar em um formato válido, como YYYY-MM-DD."
        )

    if start_date > end_date:
        raise ValueError(
            "A data inicial não pode ser maior que a data final."
        )

    # Carga dos dados
    query = """
    SELECT *
    FROM data_product_sales
    WHERE PRODUCT_CODE = %(product_code)s
            AND STORE_CODE = %(store_code)s
            AND DATE >= %(start_date)s
            AND DATE <= %(end_date)s
    """

    params = {
            "product_code": product_code,
            "store_code": store_code,
            "start_date": date[0],
            "end_date": date[1]
        }

    df = pd.read_sql(query, engine, params=params)

    # Padronização dos dados de origem
    df["STORE_CODE"] = pd.to_numeric(df["STORE_CODE"], errors="raise")
    df["PRODUCT_CODE"] = pd.to_numeric(df["PRODUCT_CODE"])
    df["DATE"] = pd.to_datetime(df["DATE"])

    return df

# Exemplo de utilização
df_resultado = retrieve_data(18, 1, ["2019-01-01", "2019-01-31"])
print(df_resultado.head())