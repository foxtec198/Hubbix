from flask import Blueprint, request as rq, jsonify
from manager.services.brands_service import BrandService

brand_bp = Blueprint("Marcas", __name__)
brand_service = BrandService()

@brand_bp.route("/")
def main():
    match rq.method:
        case "GET": return brand_service.get(rq.args, rq.headers)
        case "POST": return brand_service.create(rq.get_json(), rq.headers)
        case "PATCH": return brand_service.update(rq.get_json(), rq.headers)
        case "DELETE": return brand_service.delete(rq.args, rq.headers)
    return jsonify("Metodo não permitido"), 401