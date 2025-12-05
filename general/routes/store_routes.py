from flask import jsonify, Blueprint, request as rq
from general.services.store_service import StoreService

store_bp = Blueprint("Lojas", __name__)
store_service = StoreService()

@store_bp.route("/", methods=["GET", "POST", "pATCH", "DELETE"])
def main():
    match rq.method:
        case "GET": return store_service.get_store_data() # Retorna os dados da loja
    return jsonify()