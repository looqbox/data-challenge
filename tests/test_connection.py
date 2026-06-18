from src.models.config.connection import DBConnectionHandler
from sqlalchemy import text 


def test_create_engine_database():
    db_connection = DBConnectionHandler()
    engine = db_connection.get_engine()
    print(engine)
    


def test_work_engine_database():
    db_connection = DBConnectionHandler()
    engine = db_connection.get_engine()

    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            assert result.scalar() == 1
            print("✅ Conexão com o banco realizada com sucesso.")
    except Exception as e:
        print("❌ Erro na conexão com o banco:", e)
        assert False