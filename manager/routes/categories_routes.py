from manager.services.categories_service import CategoriesService
from flask import request as rq, Blueprint

categories_bp = Blueprint("Categories", __name__)
categories_service = CategoriesService()

@categories_bp.route("", methods=["GET", "POST", "PATCH", "DELETE"])
def main():
    match rq.method:
        case "GET": return categories_service.get(rq.args)