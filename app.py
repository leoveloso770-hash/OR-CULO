import streamlit as st
import streamlit.components.v1 as components
from streamlit_gsheets import GSheetsConnection
import json
import os

# Configuração da página
st.set_page_config(page_title="SIGAP v55 - Oráculo", layout="wide")

# COLE AQUI A URL DA SUA PLANILHA (A que você compartilhou no passo anterior)
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1T6nDpD24-wG7xLF1Gt-YxRWxA-uFFy3DXSnp7gKrhek/edit?hl=pt-br&pli=1&gid=0#gid=0"

def main():
    try:
        # Conexão usando as credenciais que você colou no painel 'Secrets' do Streamlit
        conn = st.connection("gsheets", type=GSheetsConnection)
        
        # Lê os dados da planilha
        df = conn.read(spreadsheet=URL_PLANILHA, ttl="2m")
        
        # Converte os dados para o formato que o seu Dashboard HTML entende
        dados_json = json.dumps({
            "timestamp": "Sincronizado via Nuvem",
            "totalRegistros": len(df),
            "data": df.to_dict(orient="records")
        }, ensure_ascii=False)

        # Carrega o HTML do Dashboard
        html_file = "Dashboard_v55_AutoUpdate (1).html"
        if os.path.exists(html_file):
            with open(html_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Ajuste para o HTML ler os dados da planilha em vez de procurar um arquivo local
            html_final = content.replace(
                "fetch('dados_sigap.json')", 
                f"Promise.resolve(new Response('{dados_json}'))"
            )
            
            components.html(html_final, height=1300, scrolling=True)
        else:
            st.error(f"Arquivo {html_file} não encontrado no GitHub.")

    except Exception as e:
        st.error("❌ Erro de Autenticação com o Google")
        st.write("Certifique-se de que colou o JSON no menu 'Secrets' do Streamlit Cloud.")
        st.code(e)

if __name__ == "__main__":
    main()
