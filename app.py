from flask import Flask
from flasgger import Swagger
from utils.db import db
from utils.blueprints import blueprints
from dotenv import load_dotenv
from os import getenv
from flask_socketio import SocketIO
from flask_cors import CORS

load_dotenv() # Carrega as variaveis de ambiente
app = Flask(__name__) # Cria a instacia do APP
swagger = Swagger(app) # Documentação Swaager
CORS(app) # CORS Policy 
socketio = SocketIO(app, cors_allowed_origins="*") # Cria o SocketIO
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
    "pool_size": 10, # Número de conexões abertas
    "pool_recycle": 1800, # Recria a conexão a cada 30 min
}

db.init_app(app)# Inicia o banco de dados no APP

# Carrega os Blueprints a partir do arquivo utils/blueprints.py
for bp in blueprints: app.register_blueprint(bp, url_prefix=blueprints[bp])

# Modo Dev
if __name__ == "__main__": app.run(debug=True, host="0.0.0.0", port=int(getenv("PORT", 9560)))