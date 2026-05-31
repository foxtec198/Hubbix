from flask import Blueprint, request as rq
from gourmet.services.products_service import ProductService

products_bp = Blueprint("gourmet_products", __name__)
products_service = ProductService()

@products_bp.route("", methods=["GET", "POST", "PATCH", "DELETE"])
def products():
    match rq.method:
        case "GET": return products_service.get(token_data=rq.headers)
        case "POST": return products_service.create(token_data=rq.headers)
        case "PATCH": return products_service.update(token_data=rq.headers)
        case "DELETE": return products_service.delete(token_data=rq.headers)
