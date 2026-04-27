import streamlit as st
import streamlit.components.v1 as components
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="SIGAP v55", layout="wide")

# Conexão com a planilha que você criou
url_planilha = "https://docs.google.com/spreadsheets/d/1T6nDpD24-wG7xLF1Gt-YxRWxA-uFFy3DXSnp7gKrhek"

try:
    # Mostra o Dashboard original
    with open("Dashboard_v55_AutoUpdate (1).html", "r", encoding="utf-8") as f:
        html = f.read()
    
    # Exibe o HTML na nuvem
    components.html(html, height=1200, scrolling=True)
    
except Exception as e:
    st.error("Erro ao carregar o dashboard.")
