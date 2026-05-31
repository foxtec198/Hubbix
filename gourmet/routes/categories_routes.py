from flask import Blueprint, request as rq
from gourmet.services.categories_service import CategoryService

categories_bp = Blueprint("gourmet_categories", __name__)
category_service = CategoryService()

@categories_bp.route("", methods=["GET", "POST", "PATCH", "DELETE"])
def categories():
    match rq.method:
        case "GET": return category_service.get(token_data=rq.headers)
        case "POST": return category_service.create(token_data=rq.headers)
        case "PATCH": return category_service.update(token_data=rq.headers)
        case "DELETE": return category_service.delete(token_data=rq.headers)
