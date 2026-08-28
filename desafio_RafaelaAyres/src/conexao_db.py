import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()

def get_engine():
    User = os.getenv("User")
    Pass = os.getenv("Pass")
    IP = os.getenv("IP")
    
    return create_engine(
        f"mysql+pymysql://{User}:{Pass}@{IP}/looqbox-challenge"
    )