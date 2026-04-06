from flask import Blueprint, jsonify, request as rq
from manager.services.orders_service import OrdersService

os_bp = Blueprint("Ordem de Serviço", __name__)
so_service = OrdersService()

@os_bp.route("", methods=['GET', 'POST', 'PATCH', 'DELETE'])
def main():
    match rq.method:
        case "GET": return so_service.get() # Pega todas as Ordems ouse declarado por ID
        case "POST": return so_service.create() # Cria uma nova Ordem de Serviço
        case "PATCH": return so_service.update() # Atualiza os dados de uma Orderm - Incluindo o status da Ordem
        case "DELETE": return so_service.delete() # Seta uma Ordem como cancelada