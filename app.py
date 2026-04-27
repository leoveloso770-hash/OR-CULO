import streamlit as st
import streamlit.components.v1 as components
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="SIGAP - Oráculo", layout="wide")

# Conecta com a Planilha Google (Substitua pela sua URL)
url = "COLE_AQUI_A_URL_DA_SUA_PLANILHA_GOOGLE"

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(spreadsheet=url)
    
    # Exibe o Dashboard HTML
    with open("Dashboard_v55_AutoUpdate (1).html", "r", encoding="utf-8") as f:
        html_content = f.read()
    
    # Injeta os dados do Sheets para o HTML (se necessário) ou apenas exibe o frame
    components.html(html_content, height=1200, scrolling=True)

except Exception as e:
    st.error(f"Erro ao conectar com os dados: {e}")
    st.info("Verifique se a URL da planilha está correta e se o acesso é público ou compartilhado.")
