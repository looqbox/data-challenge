"""
Execução do caso 1 automacao em python
Autora: Gabriella Pacheco

"""

import pandas as pd
from typing import Optional
from mysql_conexao import executa_query

def recupera_dados(
    product_code: Optional[int] = None,
    store_code: Optional[int] = None,
    date: Optional[list] = None
) -> pd.DataFrame:
    query = "SELECT * FROM data_product_sales WHERE 1=1"
    params = []

    if product_code is not None:
        query += " AND PRODUCT_CODE = %s"
        params.append(product_code)

    if store_code is not None:
        query += " AND STORE_CODE = %s"
        params.append(store_code)

    if date is not None:
        query += " AND DATE BETWEEN %s AND %s"
        params.extend(date)
        
    return executa_query(query, params or None)

# Executa
if __name__ == "__main__":
    print("Consulta de Vendas por Produto")
    print("(Pressione Enter para ignorar um filtro)\n")
 
    product_input = input("Código do produto: ").strip()
    store_input   = input("Código da loja: ").strip()
    date_start    = input("Data início (YYYY-MM-DD): ").strip()
    date_end      = input("Data fim   (YYYY-MM-DD): ").strip()
 
    product_code = int(product_input) if product_input else None
    store_code   = int(store_input)   if store_input   else None
    date         = [date_start, date_end] if date_start and date_end else None
 
    my_data = recupera_dados(product_code, store_code, date)
    print(f"\n{len(my_data)} registro(s) encontrado(s):\n")
    print(my_data)