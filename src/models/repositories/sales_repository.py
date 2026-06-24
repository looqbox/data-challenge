from src.models.config.connection import DBConnectionHandler
import pandas as pd
from sqlalchemy import select, column, table, and_, between
from sqlalchemy.orm import Session
from src.models.schemas.product_sales_schema import ProductSalesSchema

class SalesRepository:

    def __init__(self):
        self.__db = DBConnectionHandler()
        self.__table = table("data_product_sales")
        self.__col_map = ProductSalesSchema.COLUMN_MAP

    def read_db(self,product_code: int, store_code: int, data_range: list) -> pd.DataFrame:
        
        with self.__db.get_engine().connect() as conn:
            try:
                query = select("*").select_from(self.__table)

                if product_code is not None:
                    query = query.where(column(self.__col_map["product_code"]) == product_code)
                
                if store_code is not None:
                    query = query.where(column(self.__col_map["store_code"]) == store_code)

                if data_range is not None:
                    
                    data_start = data_range[0]
                    data_end = data_range[1]

                    if data_start and data_end:
                        query = query.where(column(self.__col_map["data_range"]).between(data_start,data_end))
                    
                    elif data_start:
                        query = query.where(column(self.__col_map["data_range"]) >= data_start)
                    
                    elif data_end:
                        query = query.where(column(self.__col_map["data_range"]) <= data_end)
                        
                print(query)
                response = pd.read_sql(query, conn)

                return response

            except Exception as exception:
                raise Exception(f"erro na query:{exception}")
                