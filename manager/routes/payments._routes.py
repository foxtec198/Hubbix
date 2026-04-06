from flask import Blueprint, request as rq, jsonify
from manager.services.payment_service import MPService

payment_bp = Blueprint("", __name__)
mp_service = MPService()

@payment_bp.route("", methods=["POST"])
def main():
    match rq.method:
        case "POST": return mp_service.get_payment_status() # Retorna o status do pagamento
