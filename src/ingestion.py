import requests
import pandas as pd

URL = "https://servicodados.ibge.gov.br/api/v3/agregados/1419/periodos/2024/variaveis/93?localidades=N1[all]"

def coletar_dados():
    response = requests.get(URL)
    data = response.json()

    series = data[0]['resultados'][0]['series']

    df = pd.DataFrame(series)
    df.to_csv("data/raw/educacao_ibge.csv", index=False)

if __name__ == "__main__":
    coletar_dados()