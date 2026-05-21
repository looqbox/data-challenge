import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Carrega as variáveis de ambiente salvas no arquivo .env
load_dotenv()

def get_engine():
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    database = os.getenv("DB_NAME")
    
    connection_string = f"mysql+pymysql://{user}:{password}@{host}/{database}"
    
    engine = create_engine(connection_string)
    return engine