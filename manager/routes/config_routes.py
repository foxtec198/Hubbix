from manager.models.config import Config
from manager.services.config_service import ConfigService
from flask import Blueprint, jsonify, request as rq

config_bp = Blueprint("Configurações", __name__)
config_service = ConfigService()

@config_bp.route("/", methods=["GET", "PATCH"])
def main():
    match rq.method:
        case "GET": return config_service.read(rq.args, rq.headers) # Retorna a config da loja
        case "PATCH": return config_service.update(rq.get_json(), rq.headers) # Retorna a config da loja
    return jsonify("Metodo não permitido"), 405

@config_bp.route("/login", methods=["POST"])
def login():
    return config_service.login(rq.get_json(), rq.headers) # Tenta logar no sistema

@config_bp.route("/update_logo", methods=["PATCH"])
def update_logo():
    return config_service.update_logo(rq.files, rq.headers) # Atualiza o ARQUIVO da Logo

@config_bp.route("/check_mat")