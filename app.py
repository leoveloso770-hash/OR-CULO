import streamlit as st
import streamlit.components.v1 as components
from streamlit_gsheets import GSheetsConnection
import json
import os

# 1. Configuração da Página
st.set_page_config(
    page_title="SIGAP v55 - Oráculo",
    page_icon="🌊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Configurações de Conexão (Substitua pela sua URL se necessário)
# Dica: No Streamlit Cloud, a URL pode ser passada via Secrets para maior segurança
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/SEU_ID_DA_PLANILHA_AQUI"

def main():
    try:
        # 3. Conexão com os dados (Google Sheets)
        # O parâmetro ttl="0" garante que ele tente ler dados frescos
        conn = st.connection("gsheets", type=GSheetsConnection)
        df = conn.read(spreadsheet=URL_PLANILHA, ttl="2m")
        
        # 4. Preparação dos dados para o Dashboard
        # Transformamos o DataFrame em JSON para que o seu HTML original possa ler
        dados_dict = df.to_dict(orient="records")
        dados_json = json.dumps({
            "timestamp": st.session_state.get("last_update", "Recém atualizado"),
            "totalRegistros": len(df),
            "data": dados_dict
        }, ensure_ascii=False)

        # 5. Carregamento do Dashboard HTML
        nome_arquivo_html = "Dashboard_v55_AutoUpdate (1).html"
        
        if os.path.exists(nome_arquivo_html):
            with open(nome_arquivo_html, "r", encoding="utf-8") as f:
                html_content = f.read()
            
            # Ajuste dinâmico: injetamos os dados do Sheets direto no HTML 
            # para garantir que ele funcione mesmo sem o arquivo dados_sigap.json local
            html_final = html_content.replace(
                "fetch('dados_sigap.json')", 
                f"Promise.resolve(new Response('{dados_json}'))"
            )

            # 6. Renderização
            components.html(html_final, height=1500, scrolling=True)
        else:
            st.error(f"Erro: O arquivo {nome_arquivo_html} não foi encontrado no GitHub.")
            st.info("Certifique-se de que o nome do arquivo HTML no repositório é exatamente igual ao configurado no código.")

    except Exception as e:
        st.error("⚠️ Ocorreu um problema na conexão com os dados.")
        st.code(f"Erro detalhado: {e}")
        st.info("Verifique se você compartilhou a planilha com o e-mail da conta de serviço.")

if __name__ == "__main__":
    main()
