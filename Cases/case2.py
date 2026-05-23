import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "mysql+pymysql://looqbox-challenge:looq-challenge@35.199.115.174:3306/looqbox-challenge"
)

query1 = f"""
SELECT
      STORE_CODE,
      STORE_NAME,
      START_DATE,
      END_DATE,
      BUSINESS_NAME,
      BUSINESS_CODE
FROM data_store_cad;
"""

query2 = f"""
SELECT
        STORE_CODE,
        DATE,
        SALES_VALUE,
        SALES_QTY
FROM data_store_sales
WHERE DATE BETWEEN '2019-01-01' AND '2019-12-31'
"""

df1 = pd.read_sql(query1, engine)
df2 = pd.read_sql(query2, engine)

df1.columns = [col.lower() for col in df1.columns]
df2.columns = [col.lower() for col in df2.columns]

df2['date'] = pd.to_datetime(df2['date'])

df2 = df2[
    (df2['date'] >= '2019-10-01') &
    (df2['date'] <= '2019-12-31')
]

df_temp = df2.groupby('store_code')[['sales_value', 'sales_qty']].sum().reset_index()

df_temp['TM'] = df_temp['sales_value'] / df_temp['sales_qty']

df_temp['TM'] = df_temp['TM'].round(2)

df_final = pd.merge(
    df1[['store_code', 'store_name', 'business_name']],
    df_temp[['store_code', 'TM']],
    on = 'store_code',
    how = 'left'
)

df_final = df_final[['store_name', 'business_name', 'TM']]

df_final = df_final.rename(columns={
    'store_name': 'Loja',
    'business_name': 'Categoria',
})

df_final = df_final.sort_values('Loja')

print(df_final.to_string(index=False))