from analytics.services.users_service import UserService
from flask import Blueprint, jsonify, request as rq

user_bp = Blueprint("Analytics - Usuarios", __name__)
user_service = UserService()

@user_bp.route("/", methods=["GET", "POST", "PATCH", "DELETE"])
def main():
    match rq.method:
        case "POST": return user_service.create_user(rq.get_json(), rq.headers)
        case "DELETE": return user_service.delete_user(rq.args, rq.headers)
    return jsonify("Metodo nao permitido"), 405