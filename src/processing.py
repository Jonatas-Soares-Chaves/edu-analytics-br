import pandas as pd
from database import inserir_dados

def processar_dados():
    df = pd.read_csv("data/raw/educacao_ibge.csv")

    df = df.rename(columns={
        "localidade": "regiao",
        "valor": "indicador"
    })

    df["indicador"] = pd.to_numeric(df["indicador"], errors="coerce")
    df = df.dropna()

    inserir_dados(df)

if __name__ == "__main__":
    processar_dados()