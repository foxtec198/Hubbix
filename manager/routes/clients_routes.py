from flask import Blueprint, jsonify, request as rq
from manager.services.clients_service import ClientService

clientes_bp = Blueprint("Clientes", __name__)
client_service = ClientService()

@clientes_bp.route("", methods=['GET', 'POST', 'DELETE', 'PATCH'])
def main():
    match rq.method:
        case 'GET': return client_service.get(rq.args) # Pega todos os clientes
        case 'POST': return client_service.create(rq.get_json(), rq.headers) # Cria o Cliente
        case 'PATCH': return client_service.update(rq.get_json(), rq.headers) # Atualiza os dados do cliente
        case 'DELETE': return client_service.delete(rq.args) # Deleta cliente por id
    return jsonify("Metodo não permitido"), 405