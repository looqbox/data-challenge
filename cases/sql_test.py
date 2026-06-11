from data.load_and_run import load_sql, run_query

def execute_sql_test():

    result = {}

    print("=== SQL TEST - RESOLUÇÃO ===")

    print("\n1. Quais os 10 produtos mais caros?")
    sql = load_sql("01_sql_test.sql")
    result["query_1"] = run_query(sql)
    print(run_query(sql))

    print("\n2. Quais as seções presentes no departamento 'BEBIDAS' e 'PADARIA'?")
    sql = load_sql("02_sql_test.sql")
    result["query_2"] = run_query(sql)
    print(run_query(sql))

    print("\n3. Qual o total de vendas de cada área de negócio no primeiro trimestre de 2019?")
    sql = load_sql("03_sql_test.sql")
    result["query_3"] = run_query(sql)
    print(run_query(sql))

    return result