from src.models.config.connection import DBConnectionHandler
import pandas as pd
from sqlalchemy import select, column, table, and_, between
from sqlalchemy.orm import Session
from src.models.schemas.product_sales_schema import ProductSalesSchema



class ImdbRepository:

    def __init__(self):
        self.__db = DBConnectionHandler()
        self.__table = table("IMDB_movies")

    def read_db(self) -> pd.DataFrame:
        
        with self.__db.get_engine().connect() as conn:
            try:
                query = select("*").select_from(self.__table)
                response = pd.read_sql(query, conn)

                return response

            except Exception as exception:
                raise Exception(f"erro na query:{exception}")
                
