from flask import Blueprint, request as rq, jsonify
from manager.services.parts_service import PartService

parts_bp = Blueprint("Peças", __name__)
parts_service = PartService()

@parts_bp.route("", methods=["GET", "POST", "PATCH", "DELETE"])
def main():
    match rq.method:
        case "GET": return parts_service.get()
        case "POST": return parts_service.create()
        case "PATCH": return parts_service.update()
        case "DELETE": return parts_service.delete()