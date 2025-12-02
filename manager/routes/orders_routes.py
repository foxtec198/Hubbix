from flask import Blueprint, jsonify, request as rq
from manager.services.orders_service import OrdersService

os_bp = Blueprint("Ordem de Serviço", __name__)
so_service = OrdersService()

@os_bp.route("/", methods=['GET', 'POST', 'PATCH', 'DELETE'])
def main():
    match rq.method:
        case "GET": return so_service.get(rq.args, rq.headers) # Pega todas as Ordems ouse declarado por ID
        case "POST": return so_service.create(rq.get_json(), rq.headers) # Cria uma nova Ordem de Serviço
        case "PATCH": return so_service.update(rq.get_json(), rq.headers) # Atualiza os dados de uma Orderm - Incluindo o status da Ordem
        case "DELETE": return so_service.delete(rq.args, rq.headers) # Seta uma Ordem como cancelada
    return jsonify("Methodo não permitido"), 405 # Retorna metodo nao permitido