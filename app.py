# ==========================================================
# SIGAP — SERVIDOR WEB (FLASK) COMPLETO - V2
# ==========================================================
# Como usar:
# 1. pip install flask
# 2. Coloque este arquivo na pasta C:\SIGAP\
# 3. Execute: python app_v2.py
# 4. Acesse: http://localhost:8080
# ==========================================================

from flask import Flask, send_from_directory, jsonify
import os

app = Flask(__name__)

# Define o diretório base onde os arquivos estão localizados
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ==========================================================
# ROTAS
# ==========================================================

@app.route("/")
def home():
    # Serve o arquivo HTML do Dashboard
    return send_from_directory(BASE_DIR, "Dashboard_v55_AutoUpdate.html")

@app.route("/dados")
def dados():
    # Serve o arquivo JSON com os dados do SIGAP
    try:
        return send_from_directory(BASE_DIR, "dados_sigap.json")
    except Exception as e:
        return jsonify({"erro": "Arquivo JSON não encontrado", "detalhe": str(e)}), 404

@app.route("/status")
def status():
    return jsonify({"status": "online"})

# ==========================================================
# EXECUÇÃO
# ==========================================================

if __name__ == "__main__":
    # Mudança para a porta 8080 para evitar conflitos (como o AirPlay no Windows/Mac)
    # Ativação do modo debug=True para ajudar a diagnosticar problemas de carregamento
    print("="*60)
    print(" SIGAP — Servidor Web iniciado (Versão Corrigida)")
    print(" Acesse: http://localhost:8080")
    print("="*60)
    app.run(host="0.0.0.0", port=8080, debug=True)

# ==========================================================
# LEMBRETE IMPORTANTE PARA O HTML
# ==========================================================
# No arquivo Dashboard_v55_AutoUpdate.html, certifique-se de usar:
# fetch(`/dados?ts=${Date.now()}`)
# Para garantir que os dados sejam atualizados sem cache.
# ==========================================================
