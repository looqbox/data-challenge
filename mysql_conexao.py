"""
Módulo de conexão com MySQL.
Autora: Gabriella Pacheco
"""

import os
import logging
import pandas as pd
import mysql.connector
from dotenv import load_dotenv

load_dotenv()
 
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)
 
# Obtendo credenciais de .env  
DB_CONFIG = {
    "host":     os.getenv("DB_HOST"),
    "port":     int(os.getenv("DB_PORT", "3306")),
    "database": os.getenv("DB_NAME", "looqbox-challenge"),
    "user":     os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
} 

#  Roda uma query no banco e devolve um DataFrame.
def executa_query(sql, params=None):
    conn = None  

    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        logger.info("Conectado ao banco com sucesso.")
        df = pd.read_sql(sql, conn, params=params)
        return df
    except mysql.connector.Error as e:
        logger.error("Erro na conexao: %s", e)
        raise
    finally:
        if conn and conn.is_connected():
            conn.close()
            logger.info("Conexao encerrada.")