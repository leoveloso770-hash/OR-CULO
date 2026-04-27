import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import os

# =========================================================
# CONFIGURAÇÕES
# =========================================================
CAMINHO_EXCEL = r"C:\Users\leove\OneDrive\SIGAP (23-04-2026).xlsx"
ID_PLANILHA_GOOGLE = "1T6nDpD24-wG7xLF1Gt-YxRWxA-uFFy3DXSnp7gKrhek"

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

        print("⏳ Lendo e procurando a tabela correta no Excel...")
        
        # Lê o Excel de forma "crua", sem definir cabeçalhos ainda
        # NOTA: Se a sua tabela oficial estiver na aba 'Base de Dados', 
        # você pode mudar para: pd.read_excel(CAMINHO_EXCEL, sheet_name='Base de Dados', header=None)
        df_raw = pd.read_excel(CAMINHO_EXCEL, engine='openpyxl', header=None)

        # --- 1. BUSCA INTELIGENTE DO CABEÇALHO ---
        # Varre as primeiras linhas até achar onde a tabela realmente começa
        linha_cabecalho = 0
        for index, row in df_raw.iterrows():
            valores_linha = row.astype(str).values
            if 'ORDEM' in valores_linha or 'DATA DE INCLUSÃO' in valores_linha:
                linha_cabecalho = index
                break
        
        # Define a linha encontrada como o verdadeiro título das colunas
        df_raw.columns = df_raw.iloc[linha_cabecalho]
        
        # Corta o dataframe para pegar apenas os dados abaixo dessa linha
        df = df_raw.iloc[linha_cabecalho + 1:].reset_index(drop=True)

        # --- 2. LIMPEZA DOS DADOS ---
        # Remove colunas vazias (completamente NaN)
        df = df.loc[:, df.columns.notna()]
        
        # Remove eventuais colunas de sobra chamadas Unnamed ou NaN
        df = df.loc[:, ~df.columns.astype(str).str.contains('^Unnamed|NaN', case=False)]
        
        # Remove as linhas lá no final que estejam vazias na coluna 'ORDEM'
        if 'ORDEM' in df.columns:
            df = df.dropna(subset=['ORDEM'])

        # --- 3. FORMATAÇÃO DE DATAS ---
        # Garante que as datas fiquem limpas e no formato DD/MM/AAAA
        for col in df.columns:
            if 'DATA' in str(col).upper():
                df[col] = pd.to_datetime(df[col], errors='coerce').dt.strftime('%d/%m/%Y')
                df[col] = df[col].replace('NaT', '') # Remove os erros de datas vazias

        print(f"📊 {len(df)} registros válidos processados. Enviando para o Google...")

        # --- 4. AUTENTICAÇÃO E ENVIO ---
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name(ARQUIVO_CREDS, scope)
        client = gspread.authorize(creds)

        # Acessa a primeira aba da Planilha Google
        sheet = client.open_by_key(ID_PLANILHA_GOOGLE).sheet1
        
        # Limpa APENAS as células preenchidas, mantendo formatações (como bordas coloridas) na medida do possível
        sheet.clear()
        
        # Converte a tabela finalizada para uma lista que o Google Sheets entenda
        dados_finais = [df.columns.values.tolist()] + df.fillna("").astype(str).values.tolist()
        
        # Envia de uma vez só
        sheet.update(dados_finais)

        print("✅ SUCESSO: Planilha Google atualizada e limpa!")

    except Exception as e:
        print(f"❌ ERRO DURANTE A EXECUÇÃO:")
        print(str(e))

if __name__ == "__main__":
    sincronizar()
