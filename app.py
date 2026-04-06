from flask import Flask, jsonify
from utils.db import db
from utils.blueprints import blueprints
from dotenv import load_dotenv
from os import getenv
from flask_socketio import SocketIO
from flask_cors import CORS

# Printa inicialização da API
print("="*20)
print("Iniciando Hubbix API")
print("="*20)

load_dotenv() # Carrega as variaveis de ambiente
print("[✅] - Variaveis de ambiente carregadas com sucesso")

print("Configurando API...")
app = Flask(__name__) # Cria a instacia do APP
CORS(app) # CORS Policy 
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="gevent") # Cria o SocketIO
app.config["SECRET_KEY"] = getenv("KEY") # Seta SUPERSECRET key, lol.
app.config["SQLALCHEMY_BINDS"] = {  # Configura os bancos de dados (Necessário pois temos mais de um Bind!)
    "analytics": getenv("ANALYTICS"), # Analytics usado para parcerias
    "lojas": getenv("LOJAS"), # Lojas do Hubbix em Geral
    "gourmet": getenv("GOURMET"), # Hubbix Gourmet
    "manager": getenv("MANAGER"), # Hubbix Manager
    "bks": getenv("BKS"), # BK Schedular
}
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = { # Configura os params do BD
    "pool_pre_ping": True, # Verifica se a conexão ainda está viva
    "pool_recycle": 1800, # Recria a conexão a cada 30 min
}
print("[✅] - API Configurada com Sucesso!") # Retorna sucesso na config. API

print("Iniciando Banco de Dados...") # Init DB
db.init_app(app)# Inicia o banco de dados no APP
print("[✅] - Banco de Dados Iniciado com Sucesso!") # Success DB

# Carrega os Blueprints a partir do arquivo utils/blueprints.py
print("Cadastrando rotas... 🚀") # Init BP
for bp in blueprints: app.register_blueprint(bp, url_prefix=blueprints[bp])
print("Todas rotas cadastradas com sucesso ✅") # Sucess BP

# Modo Desenvolvimento
if __name__ == "__main__": app.run(debug=True, host="0.0.0.0", port=int(getenv("PORT", 9560)))