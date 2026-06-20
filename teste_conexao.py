"""
Teste rápido pra validar se a conexão com o banco está funcionando.
Autora: Gabriella Pacheco
"""

from dotenv import load_dotenv
from mysql_conexao import executa_query

# Carrega as variáveis do arquivo .env
load_dotenv()


def test_conexao():
    print("Testando conexao com o banco...")
    df = executa_query("SELECT 1 AS ok")
    assert not df.empty, "Conexao falhou — DataFrame vazio."
    print("Conexao OK!\n")


def test_tabelas():
    print("Verificando tabelas disponiveis...")
    df = executa_query("SHOW TABLES")
    print(df.to_string(index=False))
    print()


def test_query_simples():
    print("Testando query na DATA_PRODUCT...")
    df = executa_query("SELECT * FROM data_product LIMIT 3")
    print(df.to_string(index=False))
    print()


if __name__ == "__main__":
    test_conexao()
    test_tabelas()
    test_query_simples()
    print("Tudo certo com a conexao.")