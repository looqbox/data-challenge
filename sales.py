import pandas as pd

class SalesRepository:

    def __init__(self, connection):
        self.connection = connection

    def retrieve_data(
        self,
        product_code=None,
        store_code=None,
        start_date=None,
        end_date=None
    ):

        if self.connection is None:
            raise ConnectionError("Sem conexão ativa!")

        query = """
            SELECT *
            FROM data_product_sales
            WHERE 1=1
        """

        params = []

        if product_code is not None:
            query += " AND PRODUCT_CODE = %s"
            params.append(product_code)

        if store_code is not None:
            query += " AND STORE_CODE = %s"
            params.append(store_code)

        if start_date is not None and end_date is not None:
            query += " AND DATE BETWEEN %s AND %s"
            params.extend([start_date, end_date])

        print("Query:", query)
        print("Params:", params)

        cursor = self.connection.cursor()

        cursor.execute(query, params)

        result = cursor.fetchall()

        columns = [desc[0] for desc in cursor.description]

        return pd.DataFrame(result, columns=columns)