from flask import Blueprint, request as rq, jsonify
from manager.services.pos_service import PosService

pos_bp = Blueprint("Caixa", __name__)
pos_service = PosService()

@pos_bp.route("/", methods=['GET', 'POST', 'PATCH', 'DELETE'])
def main():
    match rq.method:
        case "GET": return pos_service.status(rq.args, rq.headers)
        case "POST": return pos_service.open(rq.get_json(), rq.headers)
        case "PATCH": return pos_service.append(rq.get_json(), rq.headers)
        case "DELETE": return pos_service.close(rq.args, rq.headers)
    return jsonify("Metodo não permitido"), 500