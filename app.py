import streamlit as st
import streamlit.components.v1 as components
from streamlit_gsheets import GSheetsConnection
import os

st.set_page_config(page_title="SIGAP v55 - Oráculo", layout="wide")

# URL da sua Planilha Google (deve estar com acesso 'Qualquer pessoa com o link')
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1T6nDpD24-wG7xLF1Gt-YxRWxA-uFFy3DXSnp7gKrhek/edit?hl=pt-br&pli=1&gid=0#gid=0" 

try:
    # Conexão com o banco de dados (Google Sheets)
    conn = st.connection("gsheets", type=GSheetsConnection)
    # Apenas para validar a conexão silenciosamente
    data = conn.read(spreadsheet=URL_PLANILHA, ttl="5m")
    
    # Exibe seu Dashboard HTML
    if os.path.exists("Dashboard_v55_AutoUpdate (1).html"):
        with open("Dashboard_v55_AutoUpdate (1).html", "r", encoding="utf-8") as f:
            html = f.read()
        components.html(html, height=1200, scrolling=True)
    else:
        st.error("Arquivo HTML não encontrado no repositório.")

except Exception as e:
    st.error(f"Erro de Conexão: {e}")
