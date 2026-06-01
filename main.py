import pandas as pd
from sqlalchemy import create_engine, text

import matplotlib.pyplot as plt
from sqlalchemy import create_engine

### CONEXÃO
USER = "looqbox-challenge"
PASSWORD = "looq-challenge"
HOST = "35.199.115.174"
PORT = 3306

engine = create_engine(
    f"mysql+pymysql://{USER}:{PASSWORD}@{HOST}:{PORT}/looqbox-challenge"
)

''' SQL TEST - query questão 1

query = """
SELECT
    PRODUCT_COD,
    PRODUCT_NAME,
    PRODUCT_VAL
FROM `looqbox-challenge`.data_product
ORDER BY PRODUCT_VAL DESC
LIMIT 10
"""

df = pd.read_sql(query, engine)

print(df)
'''

''' SQL TEST - query questão 2
query = """
SELECT DISTINCT
    DEP_NAME,
    SECTION_COD,
    SECTION_NAME
FROM `looqbox-challenge`.data_product
WHERE DEP_NAME IN ('BEBIDAS','PADARIA')
ORDER BY DEP_NAME, SECTION_NAME;
"""

df = pd.read_sql(query, engine)

print(df)
'''

''' SQL TEST - query questão 3
query = """
SELECT
    c.BUSINESS_NAME,
    c.BUSINESS_CODE,
    ROUND(SUM(s.SALES_VALUE),2) AS TOTAL_SALES
FROM `looqbox-challenge`.data_store_sales s

JOIN `looqbox-challenge`.data_store_cad c
ON s.STORE_CODE = c.STORE_CODE

WHERE s.DATE BETWEEN '2019-01-01'
AND '2019-03-31'

GROUP BY
    c.BUSINESS_NAME,
    c.BUSINESS_CODE

ORDER BY TOTAL_SALES DESC;
"""

df = pd.read_sql(query, engine)

print(df)
'''



''' CASE 1 
### FUNÇÃO DINÂMICA

def retrieve_data(engine, product_code=None, store_code=None, date=None):

    # Condições para filtrar a consulta
    conditions=[]
    
    if not product_code and not store_code and not date:
        raise ValueError(
            "Informe pelo menos um filtro: product_code, store_code ou date."
        )

    if product_code:
        conditions.append(
            f"PRODUCT_CODE={product_code}"
        )

    if store_code:
        conditions.append(
            f"STORE_CODE='{store_code}'"
        )

    if date:
        conditions.append(
            f"DATE BETWEEN '{date[0]}' AND '{date[1]}'"
        )

    where=""

    if conditions:
        where="WHERE " + " AND ".join(conditions)

    # Monta a query
    query=f"""
        SELECT *
        FROM `looqbox-challenge`.data_product_sales
        {where}
    """

    df = pd.read_sql(query, engine)

    # Coloca com inteiro pois quantidade de produto nesse caso faz mais sentido ser inteiro
    df["SALES_QTY"] = df["SALES_QTY"].astype(int)
    
    return df
    
### EXECUÇÃO
df = retrieve_data(
    engine,
    product_code=18,
    store_code=1,
    date=[
        "2019-01-01",
        "2019-01-31"
    ]
)

# Para visualizar duas casas decimais no valor financeiro
pd.set_option('display.float_format','{:.2f}'.format)

print(df)
'''



''' CASE 2 - PARTE 1 
df1 = pd.read_sql(query1, engine)
df2 = pd.read_sql(query2, engine)

df2["DATE"] = pd.to_datetime(df2["DATE"])

df2_filtered = df2[
    df2["DATE"].between("2019-10-01", "2019-12-31")
]


print(df1)
print(df2_filtered)
'''

''' CASE 2 - PARTE 2 
query1 = """
SELECT STORE_CODE, STORE_NAME, START_DATE, END_DATE, BUSINESS_NAME, BUSINESS_CODE
FROM data_store_cad
"""

query2 = """
SELECT STORE_CODE, DATE, SALES_VALUE, SALES_QTY
FROM data_store_sales
WHERE DATE BETWEEN '2019-01-01' AND '2019-12-31'
"""

df_store = pd.read_sql(query1, engine)
df_sales = pd.read_sql(query2, engine)

# muda campo DATE para datetime
df_sales["DATE"] = pd.to_datetime(df_sales["DATE"])

# Filtra data para um intervalo
df_sales = df_sales[
    df_sales["DATE"].between("2019-10-01", "2019-12-31")
]

# Agrupa por loja
sales_grouped = (
    df_sales
    .groupby("STORE_CODE")
    .agg({ # define o que fazer com cada coluna, aqui é soma
        "SALES_VALUE": "sum",
        "SALES_QTY": "sum"
    })
    .reset_index() # transforma em coluna
)

# Calcula o Ticket Médio
sales_grouped["TM"] = (
    sales_grouped["SALES_VALUE"]
    / sales_grouped["SALES_QTY"]
)

# Junta com cadastro das lojas
result = sales_grouped.merge(
    df_store,
    on="STORE_CODE",
    how="left"
)

# Seleciona colunas
result = result[
    ["STORE_NAME", "BUSINESS_NAME", "TM"]
]

# Renomeia colunas
result.columns = [
    "Loja",
    "Categoria",
    "TM"
]

# Para visualizar duas casas decimais em TM
pd.set_option(
    'display.float_format',
    '{:.2f}'.format
)

print(result)

### GERA TABELA NO MATPLOTLIB

result_display = result.copy() # Copia dataframe
result_display["TM"] = result_display["TM"].map(
    lambda x: f"{x:.2f}" # Formata para duas casas decimais em TM
)

fig, ax = plt.subplots(figsize=(8, 6)) # Cria figura 8x6 (polegadas)
ax.axis('off') # Remove eixos

# Cria tabela
table = ax.table(
    cellText=result_display.values,   # Valores em cada celula
    colLabels=result_display.columns, # Labels das colunas
    loc='center' # Centraliza a tabela 
)

# Configura font, escala...
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1, 1.5)

plt.show()
'''



''' CASE 3
query = """
SELECT
    Genre,
    SUM(RevenueMillions) AS total_revenue
FROM IMDB_movies
WHERE Genre IS NOT NULL
AND RevenueMillions IS NOT NULL
GROUP BY Genre
ORDER BY total_revenue DESC
LIMIT 10;
"""

df = pd.read_sql(query, engine)

### GERA GRAFICO NO MATPLOTLIB

# Tamanho da figura gerada em polegadas
plt.figure(figsize=(12, 8))

# Define eixos X e Y de um gráfico de barras
plt.barh(df["Genre"], df["total_revenue"])

# Títulos e labels
plt.title("Top 10 Genres by Total Revenue")
plt.xlabel("Revenue (Millions USD)")
plt.ylabel("Genre")

# Coloca o maior valor no topo
plt.gca().invert_yaxis()

plt.tight_layout() # Ajusta espaços
plt.savefig("receita_por_genero.png", dpi=300) # Salva aquivo, dpi é qualidade da imagem
plt.show()
'''

