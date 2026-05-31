from dotenv import load_dotenv
from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from utils.db import db
from utils.blueprints import blueprints
from os import getenv, name as os_name
from subprocess import run

# Limpa o terminal para melhor visualização [NT is Windows, UNIX is Linux/Mac]
run("cls", shell=True) if os_name == "nt" else run("clear", shell=True) 

# Inicialização da API ============================================
msg = "Iniciando Hubbix API - Versão 1.4.9"
print("="*len(msg))
print(msg)
print("="*len(msg))

load_dotenv() # Carrega as variaveis de ambiente
print("\n[✅] - Variaveis de ambiente carregadas com sucesso \n")

# Configuração do app ============================================
app = Flask(__name__) # Cria a instacia do APP
CORS(app) # CORS Policy 
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="gevent") # Cria o SocketIO
app.config["SECRET_KEY"] = getenv("SECRET") # Seta SUPERSECRET key, lol.
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
print("[✅] - API Configurada com Sucesso! \n") # Retorna sucesso na config. API

# Banco de Dados ============================================
print("Iniciando Banco de Dados... ⚛️") # Init DB
db.init_app(app)# Inicia o banco de dados no APP
print("[✅] - Banco de Dados Iniciado com Sucesso! \n") # Success DB

# Carrega os Blueprints a partir do arquivo utils/blueprints.py ============================================
print("Cadastrando rotas... 🚀") # Init BP
for bp in blueprints: app.register_blueprint(bp, url_prefix=blueprints[bp])
print("[✅] - Todas rotas cadastradas com sucesso \n") # Sucess BP

# Modo Desenvolvimento
if __name__ == "__main__": 
    socketio.run(app, debug=True, host="0.0.0.0", port=int(getenv("PORT", 9560)))