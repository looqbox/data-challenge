"""
Tem a função de se conectar com o banco de dados
foi construida seguindo um padrão de acesso

IA - confirmação da variavel de conexão
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
from pathlib import Path
import os


# Isso garante que as variáveis carreguem assim que o arquivo for lido
env_path = Path(__file__).parent.parent.parent.parent / '.env'
load_dotenv(dotenv_path=env_path)


class DBConnectionHandler:
    def __init__(self) -> None:
        """Configuração de conexão com o banco do desafio Looqbox"""
        self.__connection_string = os.getenv("DATABASE_URL")
        #self.__connection_string = "mysql+pymysql://looqbox-challenge:looq-challenge@35.199.115.174/looqbox-challenge"
        #                          "tipo do banco://usuario:senha@ip de conexão/database"

        self.__engine = self.__create_database_engine()
        self.session = None

    def __create_database_engine(self):
        engine = create_engine(self.__connection_string,
                                pool_pre_ping=True)
        return engine

    def get_engine(self):
        return self.__engine

    def __enter__(self):
        session_make = sessionmaker(bind=self.__engine)
        self.session = session_make()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()             

        