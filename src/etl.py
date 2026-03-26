import pandas as pd
import os
import requests
import time
from sqlalchemy import create_engine

URL = "https://servicodados.ibge.gov.br/api/v3/agregados/5938/periodos/all/variaveis/37?localidades=N1[all]"

def extrair_api():
    headers = {"User-Agent": "Mozilla/5.0"}

    for tentativa in range(3):
        try:
            response = requests.get(URL, headers=headers, timeout=10)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Tentativa {tentativa+1} falhou: {e}")
            time.sleep(2)

    return None

def transformar_api(data):
    registros = []

    resultados = data[0]["resultados"]

    for resultado in resultados:
        for serie in resultado["series"]:
            regiao = serie["localidade"]["nome"]

            for ano, valor in serie["serie"].items():
                if valor != "...":
                    registros.append({
                        "regiao": regiao,
                        "ano": int(ano),
                        "indicador": float(valor.replace(",", "."))
                    })

    return pd.DataFrame(registros)

def carregar_dados():
    try:
        # Tenta conexão PostgreSQL
        from sqlalchemy import create_engine
        engine = create_engine("postgresql+psycopg2://postgres:senha@host:5432/educacao_db")
        df = pd.read_sql("SELECT * FROM educacao", engine)
    except:
        # Fallback CSV (funciona no deploy)
        caminho = os.path.join(os.path.dirname(__file__), "..", "data", "educacao.csv")
        df = pd.read_csv(caminho)
    return df

def executar_etl():
    data = extrair_api()

    if data:
        print("✔️ Dados da API IBGE")
        df = transformar_api(data)
    else:
        print("⚠️ Usando dados locais (fallback)")
        df = pd.read_csv("data/educacao.csv")

    carregar(df)
    print("ETL executado com sucesso!")