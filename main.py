from database import get_engine
import pandas as pd

engine = get_engine()

def listar_tabelas():
    query = "SHOW TABLES"

    df = pd.read_sql(query, engine)

    return df
print(listar_tabelas())

if __name__ == "__main__":
    print("E aí, Looqbox!")