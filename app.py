import streamlit as st
import pandas as pd
import pyodbc 
import os
from dotenv import load_dotenv


load_dotenv()
SERVER = os.getenv("DB_SERVER")
DATABASE = os.getenv("DB_NAME")
USERNAME = os.getenv("DB_USER")
PASSWORD = os.getenv("DB_PASSWORD")
 

# Conexão com o banco SQL x'

def conectar_banco():

    return pyodbc.connect(

        "DRIVER=SQL Server;"

        f"SERVER={SERVER};"

        f"DATABASE={DATABASE};"

        f"UID={USERNAME};"

        f"PWD={PASSWORD}"

    )

# Dicionário com tabelas e colunas disponíveis

tabelas_opcoes = {

    "CDG_DE_PARA_MOVEL": ["COD_AMDOCS", "PORTFOLIO"]

   

}

# Função para montar e executar a consulta SQL

def consulta_sql(tabela, colunas, filtro):

    conn = conectar_banco()

    query = f"SELECT {','.join(colunas)} FROM {tabela}"

    if filtro:

        query += f" WHERE {filtro}"

    return pd.read_sql(query, conn)

# Interface do app

st.title("Sistema de Consulta Interna")

tabela = st.selectbox("Escolha a tabela para consulta", list(tabelas_opcoes.keys()))

colunas = st.multiselect("Selecione as colunas desejadas", tabelas_opcoes[tabela], default=tabelas_opcoes[tabela])

filtro = st.text_input("Filtro opcional (ex: Tipo = 'Fixa')")

if st.button("Consultar e Baixar"):

    try:

        df = consulta_sql(tabela, colunas, filtro)

        st.dataframe(df)

        st.download_button(

            label="Baixar como TXT",

            data=df.to_csv(index=False, sep='\t'),

            file_name=f"{tabela}_resultado.txt",

            mime="text/plain"

        )

    except Exception as e:

        st.error(f"Ocorreu um erro: {e}")
    