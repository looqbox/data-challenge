'''
Construção da solução:

1 - Mostar uma query e testar no Dbeaver para consultar todas as colunas da tabela data_product_sale filtradas com:
- codigo_do_produto
-store_code
-data

2 - Trasformar em consulta via python com campos variárveis através de argumentos no script

3 - Transformar para o usuário informar input dos 3 argumentos via terminal

3.1 - Revisar critérios de preenchimento para respeitar o preenchimento de inteiros e intervalos

4 - criar um .bat para executar a consulta no terminal qunado alguém tentar rodar de fora
4.1 - criar um instalar.bat para instalar as bibliotecas necessárias para funcionar.

5 - criar uma interface amigável que a pessoa possa selecionar entre listas suspensas para selecionar intervalo de consulta, codigo de produto e store code
[realizado em Case_1_turbo.py]
'''

# Parte 1: 
'''
select * from data_product_sales dps 
where dps.PRODUCT_CODE = 18 and dps.STORE_CODE =1 and dps.`DATE` BETWEEN '2019-01-01' AND '2019-03-31'
'''

#Parte 2: 

'''
import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

conexao = pymysql.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME'),
    port=int(os.getenv('DB_PORT', 3306)),
    cursorclass=pymysql.cursors.DictCursor
)

produto_code = 18
loja_code = 18
data_inicio='2019-01-01'
data_fim= '2019-03-31'

try:
    with conexao.cursor() as cursor:
        
        sql = f"""
        SELECT * FROM data_product_sales dps 
        WHERE dps.PRODUCT_CODE = {produto_code} 
          AND dps.STORE_CODE = {loja_code} 
          AND dps.`DATE` BETWEEN '{data_inicio}' AND '{data_fim}'
        """
        # Executa a query
        cursor.execute(sql)
        
        resultados = cursor.fetchall()
        
        # Exibir os resultados
        for linha in resultados:
            print(linha)

finally:
    conexao.close()
    '''

#Parte 3


from datetime import datetime
import os
import pymysql
from dotenv import load_dotenv

def obter_dados_usuario():
    while True:
        try:
            produto_code = int(input("Digite o código do produto (int): "))
            break
        except ValueError:
            print("Entrada inválida! Por favor, digite um número inteiro.")

    while True:
        try:
            loja_code = int(input("Digite o código da loja (int): "))
            break
        except ValueError:
            print("Entrada inválida! Por favor, digite um número inteiro.")

    while True:
        data_ini_raw = input("Digite a data de início (DD-MM-AAAA): ")
        try:
            # Converte do formato brasileiro para objeto datetime
            data_obj = datetime.strptime(data_ini_raw, "%d-%m-%Y")
            data_inicio = data_obj.strftime("%Y-%m-%d")
            break
        except ValueError:
            print(
                "Formato de data inválido! Certifique-se de usar o formato DD-MM-AAAA."
            )

    while True:
        data_fim_raw = input("Digite a data de fim (DD-MM-AAAA): ")
        try:
            data_obj = datetime.strptime(data_fim_raw, "%d-%m-%Y")
            data_fim = data_obj.strftime("%Y-%m-%d")
            break
        except ValueError:
            print(
                "Formato de data inválido! Certifique-se de usar o formato DD-MM-AAAA."
            )

    date = [data_inicio, data_fim]
    #print(f"\n{produto_code}, {loja_code}, {date}\n")
    return produto_code, loja_code, data_inicio, data_fim



load_dotenv()

conexao = pymysql.connect(
    host=os.getenv('DB_HOST'),
    user=os.getenv('DB_USER'),
    password=os.getenv('DB_PASSWORD'),
    database=os.getenv('DB_NAME'),
    port=int(os.getenv('DB_PORT', 3306)),
    cursorclass=pymysql.cursors.DictCursor
)


def retrieve_data(product_code, store_code, date):
    product_code = product_code
    store_code = store_code
    data_inicio = date [0]
    data_fim = date [1]
    try:
        with conexao.cursor() as cursor:
            
            sql = f"""
            SELECT * FROM data_product_sales dps 
            WHERE dps.PRODUCT_CODE = {produto_code} 
            AND dps.STORE_CODE = {loja_code} 
            AND dps.`DATE` BETWEEN '{data_inicio}' AND '{data_fim}'
            """
            # Executa a query
            cursor.execute(sql)
            
        
            resultados = cursor.fetchall()
    finally:
        conexao.close()
    return resultados

produto_code, loja_code, data_inicio, data_fim = obter_dados_usuario()
date = [data_inicio, data_fim]
my_data = retrieve_data(produto_code, loja_code, date)

# Exibir os resultados
for linha in my_data:
    print(linha)

