from manager.models.config import Config
from manager.services.config_service import ConfigService
from flask import Blueprint, request as rq

config_bp = Blueprint("Configurações", __name__)
config_service = ConfigService()

@config_bp.route("", methods=["GET", "PATCH"])
def main():
    match rq.method:
        case "GET": return config_service.read() # Retorna a config da loja
        case "PATCH": return config_service.update() # Retorna a config da loja

# Tenta logar no sistema
@config_bp.route("/login", methods=["POST"])
def login(): return config_service.login() 

# Atualiza o ARQUIVO da Logo
@config_bp.route("/update_logo", methods=["PATCH"])
def update_logo(): return config_service.update_logo() 

# Verifica se a matrícula existe e se é valida
@config_bp.route("/check/mat/<int:mat>", methods=["GET"]) 
def check_mat(mat): return config_service.check_mat(mat)

# Verifica se o cliente tem alguma OBS por CPF
@config_bp.route("/check/cpf/<string:cpf>", methods=["GET"]) 
def check_cpf(cpf): return config_service.check_cpf(cpf)
