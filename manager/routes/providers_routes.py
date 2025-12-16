from flask import Blueprint, jsonify, request as rq
from manager.services.providers_service import ProviderService

providers_bp = Blueprint("Fornecedores", __name__)
provider_service = ProviderService()

@providers_bp.route("", methods=["GET", "POST", "PATCH", "DELETE"])
def main():
    match rq.method:
        case "GET": provider_service.get(rq.args) # obtem os fornecdores por loja ou por id
        case "POST": provider_service.create(rq.get_json(), rq.headers) # Cria um fornecedor
        case "PATCH": provider_service.update(rq.get_json()) # Atualiza os dados do fornecedor
        case "DELETE": provider_service.delete(rq.args) # Remove um fornecedor
    return jsonify("Metodo nao permitido"), 405