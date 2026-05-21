from test_sql.queries import (
    get_top_10_expensive_products,
    get_sections_by_category
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

if __name__ == "__main__":
    main()