from flask import Blueprint, request as rq, jsonify
from manager.services.cash_register_service import CashRegisterService

cr_bp = Blueprint("Caixa", __name__)
cr_service = CashRegisterService()

@cr_bp.route("/", methods=['GET', 'POST', 'PATCH', 'DELETE'])
def main():
    match rq.method:
        case "GET": return cr_service.status(rq.args, rq.headers)
        case "POST": return cr_service.open(rq.get_json(), rq.headers)
        case "PATCH": return cr_service.append(rq.get_json(), rq.headers)
        case "DELETE": return cr_service.close(rq.args, rq.headers)
    return jsonify("Metodo não permitido"), 500