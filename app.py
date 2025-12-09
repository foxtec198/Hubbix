from flask import Flask
from flasgger import Swagger
from utils.db import db
from utils.blueprints import blueprints
from dotenv import load_dotenv
from os import getenv
from flask_socketio import SocketIO
from flask_cors import CORS

load_dotenv()
app = Flask(__name__)
swagger = Swagger(app)
CORS(app) # CORS Policy 
socketio = SocketIO(app, cors_allowed_origins="*") # Ainda nao esta em uso 

# Seta SUPERSECRET key, lol.
app.config["SECRET_KEY"] = getenv("KEY")

# Configura o banco de Dados
app.config["SQLALCHEMY_BINDS"] = {
    "analytics": getenv("ANALYTICS"),
    "lojas": getenv("LOJAS"),
    "gourmet": getenv("GOURMET"),
    "manager": getenv("MANAGER"),
    "bks": getenv("BKS"),
}

# Configura os params do BD
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "pool_pre_ping": True, # Verifica se a conexão ainda está viva
    "pool_size": 10, # Número de conexões abertas
    "pool_recycle": 1800, # Recria a conexão a cada 30 min
}

# Inicia o banco de dados
db.init_app(app)

# Carrega os Blueprints
for bp in blueprints: app.register_blueprint(bp, url_prefix=blueprints[bp])

# Modo Dev
if __name__ == "__main__": 
    app.run(debug=True, host="0.0.0.0", port=int(getenv("PORT", 9560)))