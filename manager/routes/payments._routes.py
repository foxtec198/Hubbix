from flask import Blueprint, request as rq, jsonify
from manager.services.payment_services import MPService

payment_bp = Blueprint("", __name__)
mp_service = MPService()

@payment_bp.route("/", methods=["POST"])
def main():
    if rq.method == "POST": return mp_service.get_payment_status(rq.get_json(), rq.headers)
    return jsonify("Metodo nao permitido"), 405
