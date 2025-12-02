from manager.models.config import Config
from manager.services.config_service import ConfigService
from flask import Blueprint, jsonify, request as rq

config_bp = Blueprint("Configurações", __name__)
config_service = ConfigService()

@config_bp.route("/")
def main():
    match rq.method:
        case "GET": return config_service.read(rq.args, rq.headers) # Retorn a config da loja
    return jsonify("Metodo não permitido"), 405

@config_bp.route("/login", methods=["POST"])
def login():
    return config_service.login(rq.get_json(), rq.headers)