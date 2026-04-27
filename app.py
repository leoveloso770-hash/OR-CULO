import streamlit as st
import streamlit.components.v1 as components
from streamlit_gsheets import GSheetsConnection
import os

st.set_page_config(page_title="SIGAP v55 - Oráculo", layout="wide")

# Substitua pelo link da sua planilha (com permissão de leitura)
URL_PLANILHA = "SUA_URL_AQUI" 

try:
    # Conexão com Google Sheets
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(spreadsheet=URL_PLANILHA)
    
    # Carrega o seu HTML original
    if os.path.exists("Dashboard_v55_AutoUpdate (1).html"):
        with open("Dashboard_v55_AutoUpdate (1).html", "r", encoding="utf-8") as f:
            html = f.read()
        components.html(html, height=1200, scrolling=True)
    else:
        st.error("Arquivo HTML não encontrado no repositório.")

except Exception as e:
    st.error(f"Erro ao carregar dados: {e}")
