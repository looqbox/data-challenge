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