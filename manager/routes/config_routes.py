from manager.models.config import Config
from flask import Blueprint, jsonify, request as rq

config_bp = Blueprint("Configurações", __name__)

@config_bp.route("/")
def main():
    return jsonify("Sucesso")
