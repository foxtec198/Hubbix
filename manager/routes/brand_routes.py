from flask import Blueprint, request as rq
from manager.services.brands_service import BrandsService

brand_bp = Blueprint("Marcas", __name__)
brand_service = BrandsService()

@brand_bp.route("", methods=["GET", "POST", "PATCH", "DELETE"])
def main():
    match rq.method:
        case "GET": return brand_service.get() # Pega todas as marcas por loja
        case "POST": return brand_service.create() # Cria uma nova marca
        case "PATCH": return brand_service.update() # Atualiza o nome da marca
        case "DELETE": return brand_service.delete() # Deleta uma marca
        