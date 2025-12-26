from manager.services.products_service import ProductService
from flask import Blueprint, jsonify, request as rq

product_bp = Blueprint("Produtos", __name__)
prod_service = ProductService()

@product_bp.route("", methods=["GET", "POST", "PATCH", "DELETE"])
def main():
    match rq.method:
        case "GET": return prod_service.get(rq.args, rq.headers)
        case "POST": return prod_service.create(rq.get_json(), rq.headers)
        case "PATCH": return prod_service.update(rq.get_json(), rq.headers)
        case "DELETE": return prod_service.delete(rq.args, rq.headers)