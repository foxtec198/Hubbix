from flask import Blueprint, request as rq, jsonify
from manager.services.brands_service import BrandService

brand_bp = Blueprint("Marcas", __name__)
brand_service = BrandService()

@brand_bp.route("/", methods=["GET", "POST", "PATCH", "DELETE"])
def main():
    match rq.method:
        case "GET": return brand_service.get(rq.args, rq.headers) # Pega todas as marcas por loja
        case "POST": return brand_service.create(rq.get_json(), rq.headers) # Cria uma nova marca
        case "PATCH": return brand_service.update(rq.get_json(), rq.headers) # Atualiza o nome da marca
        case "DELETE": return brand_service.delete(rq.args, rq.headers) # Deleta uma marca
    return jsonify("Metodo não permitido"), 405