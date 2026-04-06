from flask import Blueprint, request as rq
from manager.services.clients_service import ClientService

clientes_bp = Blueprint("Clientes", __name__)
client_service = ClientService()

@clientes_bp.route("", methods=['GET', 'POST', 'DELETE', 'PATCH'])
def main():
    match rq.method:
        case 'GET': return client_service.get() # Pega todos os clientes
        case 'POST': return client_service.create() # Cria o Cliente
        case 'PATCH': return client_service.update() # Atualiza os dados do cliente
        case 'DELETE': return client_service.delete() # Deleta cliente por id
        