import streamlit as st
import pandas as pd
import plotly.express as px

st.sidebar.header('CaféGG')
opcoes = [
    'Previsão de Colheita',
    'Produção Semanal',
    'Terreiro',
    'GASOLINA',
    'GASTOS DIVERSOS',
    'Config'
]

selecionada = st.sidebar.selectbox('Escolha a aba:', opcoes, index=0)

if selecionada == opcoes[0]:
    df_plantas = pd.read_csv('assets/previsao/previsao.csv', sep=',', on_bad_lines='skip')

    # Corrige a coluna "Litros por Planta"
    df_plantas['Litros por Planta'] = (
        df_plantas['Litros por Planta']
        .astype(str)
        .str.replace(',', '.')
    )
    df_plantas['Litros por Planta'] = pd.to_numeric(
        df_plantas['Litros por Planta'], errors='coerce'
    ).fillna(0)

    # Remove linha TOTAL se existir
    df_sem_total = df_plantas[df_plantas["Lavoura"] != "TOTAL"]

    # Calcula os totais
    total_plantas = df_plantas['Plantas'].sum()
    media = round(df_plantas['Litros por Planta'].mean(), 2)

    # Cria linha TOTAL
    df_total = pd.DataFrame(
        [["TOTAL", total_plantas, media]],
        columns=df_plantas.columns
    )

    # Junta ao DataFrame
    df_plantas = pd.concat([df_sem_total, df_total], ignore_index=True)

    st.title('Previsão de Colheita')
    st.write('Previsão baseado em diversos preços do café')

    st.table(df_plantas)

    st.write('Gráfico de renda previsto de acordo com o café')

    renda = total_plantas * round(df_plantas['Litros por Planta'].mean(), 2) / 60 / 7

    df_price = pd.read_csv("assets/previsao/prices.csv")
    
    df_price["RendaCalculada"] = (df_price["price"] * renda).round(-3)

    fig = px.bar(
        df_price,
        x="price",
        y="RendaCalculada",
        color="RendaCalculada",  # cores diferentes por categoria
        hover_data=["RendaCalculada", "price"],  # mostra info ao passar o mouse
        title="Previsão de renda"
    )

    # Deixa o gráfico menor e mais compacto
    fig.update_layout(
        height=600,
        width=600,
        xaxis_title="Lavoura",
        yaxis_title="Litros por Planta",
        showlegend=False
    )

    st.plotly_chart(fig, use_container_width=True)

    col1, col2 = st.columns(2)

    # Iterar sobre os valores e alternar entre colunas
    for idx, i in enumerate(df_price["RendaCalculada"]):
        if idx % 2 == 0:
            col1.markdown(f"<p style='margin:0'>Preço: {df_price['price'][idx]}$ Renda: {int(i)}$</p>", unsafe_allow_html=True)
        else:
            col2.markdown(f"<p style='margin:0'>Preço: {df_price['price'][idx]}$ Renda: {int(i)}$</p>", unsafe_allow_html=True)

elif selecionada == opcoes[5]:
    st.write('mf')
