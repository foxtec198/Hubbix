from manager.services.products_service import ProductService
from flask import Blueprint, jsonify, request as rq

product_bp = Blueprint("Produtos", __name__)
prod_service = ProductService()

@product_bp.route("", methods=["GET", "POST", "PATCH", "DELETE"])
def main():
    match rq.method:
        case "GET": return prod_service.get()
        case "POST": return prod_service.create()
        case "PATCH": return prod_service.update()
        case "DELETE": return prod_service.delete()

@product_bp.route("/categorias")
def get_by_categories():
    if rq.method == "GET":
        return prod_service.get_categories()