from flask import Blueprint, jsonify, request as rq
from manager.services.service_order_services import ServiceOrderServices

os_bp = Blueprint("Ordem de Serviço", __name__)
so_service = ServiceOrderServices()

@os_bp.route("/", methods=['GET', 'POST', 'PATCH', 'DELETE']) # pyright: ignore[reportArgumentType]
def main():
    match rq.method:
        case "GET": return so_service.get(rq.args, rq.headers)
        case "POST": return so_service.create(rq.get_json(), rq.headers)
        case "PATCH": return so_service.make_so(799, "1 - MS - OFICINA DO CELULAR")
    return jsonify("Erro Interno"), 500