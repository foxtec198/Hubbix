from analytics.services.clients_service import ClientService
from flask import Blueprint, jsonify, request as rq

clients_bp = Blueprint("Clientes", __name__)
clientes_service = ClientService()

@clients_bp.route("/", methods=["GET", "POST", "PATCH", "DELETE"])
def main():
    match rq.method:
        case "GET": return clientes_service.get(rq.args, rq.headers)
        case "POST": return clientes_service.create_client(rq.get_json(), rq.headers)
        case "PATCH": return clientes_service.update_client(rq.get_json(), rq.headers)
        case "DELETE": return clientes_service.delete_client(rq.args, rq.headers)
    return jsonify("Metodo nao permitido"), 405