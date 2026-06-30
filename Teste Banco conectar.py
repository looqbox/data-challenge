import os

import pymysql
from dotenv import load_dotenv

load_dotenv()

conexao = pymysql.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME'),
    port=int(os.getenv('DB_PORT', 3306)),
    cursorclass=pymysql.cursors.DictCursor
)

try:
    with conexao.cursor() as cursor:
        
        sql = """
        SELECT 
            dsc.BUSINESS_NAME,
            SUM(dps.SALES_VALUE) AS TOTAL_SALES_VALUE
        FROM 
            data_product_sales dps 
        INNER JOIN 
            data_store_cad dsc ON dps.STORE_CODE = dsc.STORE_CODE
        WHERE 
            dps.DATE BETWEEN '2019-01-01' AND '2019-03-31'
        GROUP BY 
            dsc.BUSINESS_NAME;
        """
        
        # Executa a query
        cursor.execute(sql)
        
        resultados = cursor.fetchall()
        
        # Exibir os resultados
        for linha in resultados:
            print(linha)

finally:
    conexao.close()