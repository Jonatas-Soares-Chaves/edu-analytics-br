import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.database import consultar_dados
from src.model import treinar_modelo

import streamlit as st
import plotly.express as px

# CONFIG
st.set_page_config(page_title="Educação no Brasil", layout="wide")

# 🔥 HEADER
st.markdown("""
# 📊 Educação no Brasil  
### 📌 Análise de desigualdade educacional + previsão com Machine Learning  
""")

# 🔥 CARREGAR
@st.cache_data
def carregar():
    return consultar_dados()

with st.spinner("Carregando dados..."):
    df_original = carregar()

if df_original.empty:
    st.error("Nenhum dado encontrado.")
    st.stop()

# 🔥 MACHINE LEARNING
df_modelo = treinar_modelo(df_original.copy())

st.divider()

# 🔥 FILTROS
st.sidebar.header("Filtros")

# Filtrar por regiões
regioes = st.sidebar.multiselect(
    "Regiões",
    df_modelo["regiao"].unique(),
    default=df_modelo["regiao"].unique()
)

# Filtrar por anos
anos = st.sidebar.slider(
    "Selecione o intervalo de anos",
    int(df_modelo["ano"].min()),
    int(df_modelo["ano"].max()),
    (int(df_modelo["ano"].min()), int(df_modelo["ano"].max()))
)

# Aplica filtros
df_filtrado = df_modelo[
    (df_modelo["regiao"].isin(regioes)) &
    (df_modelo["ano"] >= anos[0]) &
    (df_modelo["ano"] <= anos[1])
]

# Exibição
st.write("### Dados Filtrados")
st.dataframe(df_filtrado)

st.write("### Gráfico de Linha")
grafico = df_filtrado.pivot(index="ano", columns="regiao", values="indicador")
st.line_chart(grafico)

# 🔥 PROTEÇÃO
if df_modelo.empty:
    st.warning("Nenhum dado com esses filtros.")
    st.stop()

# 🔥 KPIs (somente dados reais)
df_real = df_modelo[df_modelo["tipo"] == "real"]

col1, col2, col3 = st.columns(3)

col1.metric("Média", f"{df_real['indicador'].mean():.2f}")
col2.metric("Máximo", f"{df_real['indicador'].max():.2f}")
col3.metric("Mínimo", f"{df_real['indicador'].min():.2f}")

st.divider()

# 🔥 INSIGHTS
st.markdown("## 🧠 Insights Automáticos")

melhor = df_real.loc[df_real["indicador"].idxmax()]
pior = df_real.loc[df_real["indicador"].idxmin()]

st.success(f"Melhor região: **{melhor['regiao']}** ({melhor['indicador']:.2f})")
st.error(f"Pior região: **{pior['regiao']}** ({pior['indicador']:.2f})")

gap = melhor["indicador"] - pior["indicador"]
st.info(f"Gap: **{gap:.2f} pontos**")

st.divider()

# 🔥 GRÁFICO ML
st.markdown("## 🤖 Previsão com Machine Learning")

fig = px.line(
    df_modelo,
    x="ano",
    y="indicador",
    color="regiao",
    line_dash="tipo",
    markers=True
)

st.plotly_chart(fig, use_container_width=True)

st.divider()

# 🔥 TABELA
st.subheader("📋 Dados")
st.dataframe(df_modelo, use_container_width=True)