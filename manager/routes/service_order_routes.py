from flask import Blueprint, jsonify, request as rq
from manager.services.service_order_service import ServiceOrderServices

os_bp = Blueprint("Ordem de Serviço", __name__)
so_service = ServiceOrderServices()

@os_bp.route("/", methods=['GET', 'POST', 'PATCH', 'DELETE']) # pyright: ignore[reportArgumentType]
def main():
    match rq.method:
        case "GET": return so_service.get(rq.args, rq.headers)
        case "POST": return so_service.create(rq.get_json(), rq.headers)
        case "PATCH": return so_service.update(rq.get_json(), rq.headers)
        case "DELETE": return so_service.delete(rq.args, rq.headers)
    return jsonify("Erro Interno"), 500