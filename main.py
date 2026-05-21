from test_sql.queries import get_top_10_expensive_products

def main():
    #1. Obter os 10 produtos mais caros
    df_products = get_top_10_expensive_products()
    print(df_products)

if __name__ == "__main__":
    main()