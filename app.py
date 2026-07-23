import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Explorador de Catálogo - Hardware & Eletrônicos", layout="wide")

# ==========================================================
# Carregamento de dados
# ==========================================================
@st.cache_data
def carregar_dados():
    df = pd.read_csv("produtos_hardware_eletronicos_app.csv")
    df = df[df["price"] > 0]  # remove produtos sem preço válido (Item 4)
    df = df[df["stars"] > 0]  # remove produtos sem avaliação (Item 4)
    return df

df = carregar_dados()

# ==========================================================
# Cabeçalho
# ==========================================================
st.title("🖥️ Explorador de Catálogo — Hardware & Eletrônicos")
st.markdown(
    "Data App desenvolvido para o case técnico Dadosfera. "
    "Explore os 118 mil produtos de hardware e eletrônicos filtrando por categoria, preço e avaliação."
)

# ==========================================================
# Barra lateral — filtros
# ==========================================================
st.sidebar.header("Filtros")

categorias = sorted(df["category_name"].unique())
categoria_selecionada = st.sidebar.multiselect(
    "Categoria", categorias, default=categorias[:3]
)

preco_min, preco_max = st.sidebar.slider(
    "Faixa de preço (US$)",
    float(df["price"].min()), float(df["price"].max()),
    (0.0, 200.0)
)

avaliacao_min = st.sidebar.slider("Avaliação mínima", 1.0, 5.0, 3.0, 0.1)

busca_titulo = st.sidebar.text_input("Buscar por palavra no título")

# ==========================================================
# Aplicação dos filtros
# ==========================================================
df_filtrado = df.copy()

if categoria_selecionada:
    df_filtrado = df_filtrado[df_filtrado["category_name"].isin(categoria_selecionada)]

df_filtrado = df_filtrado[
    (df_filtrado["price"] >= preco_min) & (df_filtrado["price"] <= preco_max)
]

df_filtrado = df_filtrado[df_filtrado["stars"] >= avaliacao_min]

if busca_titulo:
    df_filtrado = df_filtrado[df_filtrado["title"].str.contains(busca_titulo, case=False, na=False)]

# ==========================================================
# Métricas gerais
# ==========================================================
col1, col2, col3, col4 = st.columns(4)
col1.metric("Produtos encontrados", f"{len(df_filtrado):,}")
col2.metric("Preço médio", f"US$ {df_filtrado['price'].mean():.2f}" if len(df_filtrado) else "—")
col3.metric("Avaliação média", f"{df_filtrado['stars'].mean():.2f} ⭐" if len(df_filtrado) else "—")
col4.metric("Categorias", df_filtrado["category_name"].nunique())

st.divider()

# ==========================================================
# Gráficos
# ==========================================================
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Preço médio por categoria")
    if len(df_filtrado):
        preco_categoria = df_filtrado.groupby("category_name")["price"].mean().sort_values(ascending=False)
        fig = px.bar(preco_categoria, orientation="h", labels={"value": "Preço médio (US$)", "category_name": "Categoria"})
        st.plotly_chart(fig, use_container_width=True)

with col_b:
    st.subheader("Preço vs Avaliação")
    if len(df_filtrado):
        fig2 = px.scatter(
            df_filtrado.sample(min(2000, len(df_filtrado))),
            x="price", y="stars", color="category_name",
            labels={"price": "Preço (US$)", "stars": "Avaliação"},
            opacity=0.5
        )
        st.plotly_chart(fig2, use_container_width=True)

st.divider()

# ==========================================================
# Tabela de resultados
# ==========================================================
st.subheader("Produtos encontrados")
st.dataframe(
    df_filtrado[["title", "category_name", "price", "stars", "reviews", "boughtInLastMonth"]]
    .rename(columns={
        "title": "Título", "category_name": "Categoria", "price": "Preço (US$)",
        "stars": "Avaliação", "reviews": "Nº Avaliações", "boughtInLastMonth": "Comprado (último mês)"
    })
    .sort_values("Comprado (último mês)", ascending=False),
    use_container_width=True,
    height=400
)

st.caption("Case técnico Dadosfera — Julio Baltazar | Dados: Amazon Products 2023 (Kaggle), filtrado para hardware/eletrônicos.")
