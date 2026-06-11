import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

# Config doo MySQL extraído das variáveis de ambiente .env
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_DATABASE"),
}

# função retorna a conexãoo com o banco MySQL
def get_connection():
    return mysql.connector.connect(**DB_CONFIG)