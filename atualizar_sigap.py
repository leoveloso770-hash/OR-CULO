import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os

# =========================================================
# CONFIGURAÇÕES
# =========================================================
CAMINHO_EXCEL = r"C:\Users\leove\OneDrive\SIGAP (23-04-2026).xlsx"

# APENAS O ID (removi a URL inteira para evitar o erro 404)
ID_PLANILHA_GOOGLE = "1T6nDpD24-wG7xLF1Gt-YxRWxA-uFFy3DXSnp7gKrhek"

# Garante que o script ache o JSON na pasta C:\SIGAP independente de onde você chame o terminal
BASE_DIR = r"C:\SIGAP"
ARQUIVO_CREDS = os.path.join(BASE_DIR, "credenciais.json")

def sincronizar():
    print("="*60)
    print(f" SIGAP — SINCRONIZADOR NUVEM | {datetime.now().strftime('%d/%m %H:%M')}")
    print("="*60)

    try:
        if not os.path.exists(CAMINHO_EXCEL):
            print(f"❌ ERRO: Arquivo Excel não encontrado em:\n{CAMINHO_EXCEL}")
            return

        print("⏳ Lendo e limpando dados do Excel...")
        # Lemos o Excel
        df = pd.read_excel(CAMINHO_EXCEL, engine='openpyxl')

        # --- LIMPEZA DE FORMATAÇÃO ---
        # 1. Remove colunas vazias (as que apareciam como 'Unnamed')
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        
        # 2. Remove linhas onde a coluna 'ORDEM' está vazia (evita lixo no final)
        if 'ORDEM' in df.columns:
            df = df.dropna(subset=['ORDEM'])

        # 3. Formata as colunas de DATA para o padrão brasileiro
        for col in df.columns:
            if 'DATA' in col.upper():
                df[col] = pd.to_datetime(df[col]).dt.strftime('%d/%m/%Y')

        print(f"📊 {len(df)} registros processados. Enviando...")

        # AUTENTICAÇÃO
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(ARQUIVO_CREDS, scope)
        client = gspread.authorize(creds)

        # ENVIO
        sheet = client.open_by_key(ID_PLANILHA_GOOGLE).sheet1
        
        # ATENÇÃO: Usei update() sem clear() total para tentar preservar bordas manuais
        # Convertemos para lista de strings para o Google Sheets aceitar sem erros
        dados_finais = [df.columns.values.tolist()] + df.fillna("").astype(str).values.tolist()
        
        sheet.update(dados_finais)

        print("✅ SUCESSO: Planilha Google atualizada!")

    except Exception as e:
        print(f"❌ ERRO DURANTE A EXECUÇÃO:")
        print(str(e))

if __name__ == "__main__":
    sincronizar()
