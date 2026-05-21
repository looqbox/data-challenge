from cases.case1 import recuper_data

from test_sql.queries import (
    get_top_10_expensive_products,
    get_sections_by_category,
    get_total_sales_by_business_area
)

def main():
    #1. Obter os 10 produtos mais caros
    print("Top 10 produtos mais caros:")
    df_products = get_top_10_expensive_products()
    print(df_products)

    #2. Obter as seções distintas para as categorias 'BEBIDAS' e 'PADARIA'
    print("\nSeções para as categorias 'BEBIDAS' e 'PADARIA':")
    df_sections = get_sections_by_category()
    print(df_sections)

    #3. Obter o total de vendas por área de negócio para o primeiro trimestre de 2019
    print("\nTotal de vendas por área de negócio (1º trimestre de 2019):")
    df_sales = get_total_sales_by_business_area()
    print(df_sales)

    #4. Exemplo de uso da função de recuperação de dados com filtros
    print("\nDados de vendas para o produto 'P018' na loja 'S001' entre '2019-01-01' e '2019-03-31':")
    df_filtered = recuper_data(
        product_code=18,
        store_code=1, 
        date_range=['2019-01-01', '2019-03-31']
    )
    print(df_filtered)

if __name__ == "__main__":
    main()