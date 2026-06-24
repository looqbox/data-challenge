"""
Como não são enviados dados nessa query,
não foi necessario a contrução de schemas 
"""
from src.models.config.connection import DBConnectionHandler
import pandas as pd
from sqlalchemy.orm import Session
from sqlalchemy import text



class StoreRepository:

    def __init__(self):
        self.__db = DBConnectionHandler()


    def get_store_cad(self) -> pd.DataFrame:

        try:
            query = text("""
                SELECT
                    STORE_CODE,
                    STORE_NAME,
                    START_DATE,
                    END_DATE,
                    BUSINESS_NAME,
                    BUSINESS_CODE
                FROM data_store_cad
            """)
            with self.__db.get_engine().connect() as conn:
                return pd.read_sql(query, conn)
        
        except Exception as exception:
            raise Exception(f"erro na query {exception}")

    def get_store_sales(self) -> pd.DataFrame:
        
        try:
            query = text("""
                SELECT
                    STORE_CODE,
                    DATE,
                    SALES_VALUE,
                    SALES_QTY
                FROM data_store_sales
                WHERE DATE BETWEEN '2019-01-01' AND '2019-12-31'
            """)
            with self.__db.get_engine().connect() as conn:
                return pd.read_sql(query, conn)
        
        except Exception as exception:
            raise Exception(f"erro na query {exception}")