from flask import Blueprint, jsonify, request as rq
from manager.services.providers_service import ProviderService

providers_bp = Blueprint("Fornecedores", __name__)
provider_service = ProviderService()

@providers_bp.route("", methods=["GET", "POST", "PATCH", "DELETE"])
def main():
    match rq.method:
        case "GET": provider_service.get() # obtem os fornecdores por loja ou por id
        case "POST": provider_service.create() # Cria um fornecedor
        case "PATCH": provider_service.update() # Atualiza os dados do fornecedor
        case "DELETE": provider_service.delete() # Remove um fornecedor