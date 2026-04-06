from flask import jsonify, request as rq, Blueprint
from manager.services.sales_service import SalesService

sales_bp = Blueprint('Vendas', __name__)
sales_service = SalesService()

@sales_bp.route("", methods=["GET", "POST", "DELETE", "PATCH"])
def main():
    match rq.method:
        case "GET": return sales_service.get()
        case "POST": return sales_service.create()