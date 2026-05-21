import pandas as pd
from database import get_engine

engine = get_engine()

def get_top_10_expensive_products():
    query = """
    SELECT
        PRODUCT_COD,
        PRODUCT_NAME,
        PRODUCT_VAL,
        DEP_NAME,
        DEP_COD,
        SECTION_NAME,
        SECTION_COD
    FROM data_product
    ORDER BY PRODUCT_VAL DESC, PRODUCT_COD ASC
    LIMIT 10
    """
    return pd.read_sql(query, engine)

def get_sections_by_category():
    query = """
    SELECT DISTINCT
        DEP_NAME,
        SECTION_NAME
    FROM data_product
    WHERE 
        DEP_NAME IN ('BEBIDAS', 'PADARIA')
    ORDER BY DEP_NAME, SECTION_NAME
    """
    return pd.read_sql(query, engine)

def get_total_sales_by_business_area():
    query = """
    SELECT
        sc.BUSINESS_NAME,
        SUM(ps.SALES_VALUE) AS TOTAL_SALES
    FROM data_product_sales as ps
    JOIN data_store_cad as sc
        ON ps.STORE_CODE = sc.STORE_CODE
    WHERE
        ps.DATE BETWEEN '2019-01-01' AND '2019-03-31'
    GROUP BY sc.BUSINESS_NAME
    ORDER BY TOTAL_SALES DESC
    """
    return pd.read_sql(query, engine)