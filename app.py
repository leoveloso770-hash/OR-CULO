import streamlit as st
import streamlit.components.v1 as components
from streamlit_gsheets import GSheetsConnection
import json
import os

# Configuração da página
st.set_page_config(page_title="SIGAP v55 - Oráculo", layout="wide")

# URL da sua Planilha (Certifique-se de que é a URL completa do navegador)
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/1T6nDpD24-wG7xLF1Gt-YxRWxA-uFFy3DXSnp7gKrhek/edit?hl=pt-br&pli=1&gid=0#gid=0"

def main():
    try:
        # A conexão 'gsheets' vai buscar automaticamente o que estiver no seu Secrets
        conn = st.connection("gsheets", type=GSheetsConnection)
        
        # Tentativa de leitura
        df = conn.read(spreadsheet=URL_PLANILHA, ttl="2m")
        
        # Se chegou aqui, a conexão funcionou! 
        # Vamos preparar os dados para o seu HTML
        dados_json = json.dumps({
            "timestamp": "Sincronizado via Google Sheets",
            "totalRegistros": len(df),
            "data": df.to_dict(orient="records")
        }, ensure_ascii=False)

        # Carregar o seu Dashboard HTML
        html_file = "Dashboard_v55_AutoUpdate .html"
        if os.path.exists(html_file):
            with open(html_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Injeta os dados da planilha direto no HTML
            html_final = content.replace(
                "fetch('dados_sigap.json')", 
                f"Promise.resolve(new Response('{dados_json}'))"
            )
            
            components.html(html_final, height=1300, scrolling=True)
        else:
            st.error(f"Arquivo {html_file} não encontrado no repositório.")

    except Exception as e:
        st.error("❌ Erro de Autenticação (401)")
        st.info("O Google recusou a conexão. Verifique os 2 pontos abaixo:")
        st.code(e)

if __name__ == "__main__":
    main()
