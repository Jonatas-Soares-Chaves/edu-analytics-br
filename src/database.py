from sqlalchemy import create_engine
import pandas as pd

def get_engine():
    return create_engine(
        "postgresql+psycopg2://postgres:jonatas12@localhost:54321/educacao_db"
    )

def consultar_dados():
    engine = get_engine()
    return pd.read_sql("SELECT * FROM educacao", engine)