import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

# Conexão com o banco de dados MySQL
engine = create_engine(
    "mysql+pymysql://looqbox-challenge:looq-challenge@35.199.115.174:3306/looqbox-challenge"
)

# Consulta 1 - Cadastro das lojas
query_1 = """
SELECT
      STORE_CODE,
      STORE_NAME,
      START_DATE,
      END_DATE,
      BUSINESS_NAME,
      BUSINESS_CODE
FROM data_store_cad
"""

df_store = pd.read_sql(query_1, engine)

# Consulta 2 - Vendas das lojas
query_2 = """
SELECT
        STORE_CODE,
        DATE,
        SALES_VALUE,
        SALES_QTY
FROM data_store_sales
WHERE DATE BETWEEN '2019-01-01' AND '2019-12-31'
"""

df_sales = pd.read_sql(query_2, engine)

# Tratamento dos dados
df_sales["DATE"] = pd.to_datetime(df_sales["DATE"])

# Filtrando os dados de vendas para o período de 01/10/2019 a 31/12/2019
start_date = "2019-10-01"
end_date = "2019-12-31"

df_sales_filtrado = df_sales[
    (df_sales["DATE"] >= start_date) &
    (df_sales["DATE"] <= end_date)
]

# print(df_sales_filtrado)

# Relacionando os dados de vendas com os dados de cadastro das lojas
df = df_sales_filtrado.merge(
    df_store,
    on="STORE_CODE",
    how="left"
)

# print(df)
# print(df[['STORE_NAME', 'BUSINESS_NAME']])

# Cálculo do TM
df_result = (
    df.groupby(
        ["STORE_NAME", "BUSINESS_NAME"],
        as_index=False
    )
    .agg(
        SALES_VALUE=("SALES_VALUE", "sum"),
        SALES_QTY=("SALES_QTY", "sum")
    )
)

df_result["TM"] = df_result["SALES_VALUE"] / df_result["SALES_QTY"]

# Selecionando as colunas
df_result = df_result[
    ["STORE_NAME", "BUSINESS_NAME", "TM"]
]

# Renomeando as colunas
df_result = df_result.rename(
    columns={
        "STORE_NAME": "Loja",
        "BUSINESS_NAME": "Categoria",
    }
)

df_result["TM"] = df_result["TM"].round(2)
print(df_result)

# Cópia para formatação do TM com vírgula
df_bras = df_result.copy()
df_bras["TM"] = df_bras["TM"].map(
    lambda x: f"{x:.2f}".replace(".", ",")
)

# Criando tabela visual com Matplotlib
fig, ax = plt.subplots(figsize=(8, 8))
ax.axis("off")

# Criando a tabela
table = ax.table(
    cellText=df_bras.values,
    colLabels=df_bras.columns,
    loc="center",
    cellLoc="center",
    bbox=[0, 0, 1, 0.9]
)

table.auto_set_font_size(False)
table.set_fontsize(11)

# Pintando o cabeçalho para dar destaque
for (row, col), cell in table.get_celld().items():
    if row == 0:
        cell.set_text_props(weight='bold', color='white')
        cell.set_facecolor('#1f77b4')

plt.title(
    "Ticket Médio (TM) por Loja e Categoria\n(Out - Dez / 2019)", 
    fontsize=14, 
    fontweight="bold", 
    y=0.95
    )

plt.tight_layout()
plt.show()
