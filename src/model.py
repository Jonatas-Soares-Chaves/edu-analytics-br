import pandas as pd
from sklearn.linear_model import LinearRegression

def treinar_modelo(df):
    previsoes = []

    regioes = df["regiao"].unique()

    for regiao in regioes:
        df_regiao = df[df["regiao"] == regiao].sort_values("ano")

        if len(df_regiao) < 2:
            continue
        X = df_regiao[["ano"]]
        y = df_regiao["indicador"]

        modelo = LinearRegression()
        modelo.fit(X, y)

        anos_futuros = [2025, 2026, 2027]

        for ano in anos_futuros:
            pred = modelo.predict([[ano]])[0]

            previsoes.append({
                "regiao": regiao,
                "ano": ano,
                "indicador": round(pred, 2),
                "tipo": "previsao"
            })

    df["tipo"] = "real"

    df_previsao = pd.DataFrame(previsoes)

    return pd.concat([df, df_previsao])
