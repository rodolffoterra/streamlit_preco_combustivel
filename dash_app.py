import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image


st.set_page_config(layout= "wide")

st.cache_data
def gerar_df():
    df =pd.read_excel(
        io = "database_anp.xlsx",
        engine= "openpyxl",
        sheet_name= "Sheet1",
        usecols= "A:Q"
    )
    return  df

df = gerar_df()
colunasUteis = ['MÊS','PRODUTO','REGIÃO','ESTADO','PREÇO MÉDIO REVENDA']
df = df[colunasUteis]

with st.sidebar:
    st.subheader("Produtividade 100%")
    logo_teste = Image.open("logo.jpg")
    st.image(logo_teste, use_column_width= True)
    st.subheader("Seleção de filtros")
    fProduto = st.selectbox(
        "Selecione o Combustível",
        options= df['PRODUTO'].unique()
    )

    fEstado = st.selectbox(
        "Selecione o Estado",
        options= df['ESTADO'].unique()
    )

    dadosUsuario = df.loc[(
        df['PRODUTO'] == fProduto) &
        (df["ESTADO"] == fEstado
    )]

updateDatas = dadosUsuario["MÊS"].dt.strftime("%Y/%b")
dadosUsuario['MÊS'] = updateDatas[0:] 


st.header("Preços dos Combustíveis no Brasil: 2013 à 2023 ")
st.markdown('**Combustível selecionado** ' + fProduto)
st.markdown('**Estado selecionado** ' + fEstado)

grafCombRstado = alt.Chart(dadosUsuario).mark_line(
    point = alt.OverlayMarkDef(color = 'red', size= 20)
).encode(
    x = 'MÊS:T',
    y = 'PREÇO MÉDIO REVENDA',
    strokeWidth=alt.value(3)
).properties( 
    height = 700,
    width = 1200
)

st.altair_chart(grafCombRstado)