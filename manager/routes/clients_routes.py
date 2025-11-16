from flask import Blueprint, jsonify, request as rq
from manager.services.clients_service import ClientService

clientes_bp = Blueprint("Clientes", __name__)
client_service = ClientService()

@clientes_bp.route("/", methods=['GET', 'POST', 'DELETE', 'PATCH'])
def main():
    match rq.method:
        case 'GET': # Pega todos os clientes
            return client_service.get(rq.args, rq.headers)
            
        case 'POST': # Cria o Cliente
            return client_service.create(rq.get_json(), rq.headers)
        
        case 'PATCH': # Atualiza os dados do cliente
            return client_service.update(rq.get_json(), rq.headers) 
        
        case 'DELETE': # Deleta cliente por id
            return client_service.delete(rq.args, rq.headers)
        
    return jsonify("Erro interno"), 500