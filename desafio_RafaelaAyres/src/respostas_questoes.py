import pandas as pd
from .conexao_db import get_engine

engine = get_engine()

# src/respostas_questoes/questao_1.sql

with open("sql/questao_1.sql", "r") as file:
    query = file.read()

df = pd.read_sql(query, engine)

print("Questão 1:")
print(df)

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=

# src/respostas_questoes/questao_2.sql

with open("sql/questao_2.sql", "r") as file:
    query = file.read()

df2 = pd.read_sql(query, engine)

print("\nQuestão 2:")
print(df2)

#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=#=

# src/respostas_questoes/questao_3.sql

with open("sql/questao_3.sql", "r") as file:
    query = file.read()

df3 = pd.read_sql(query, engine)

df3["total_vendas"] = df3["total_vendas"].map(lambda x: f"$ {x:,.2f}")

print("\nQuestão 3:")
print(df3)
