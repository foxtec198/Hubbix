from flask import Blueprint, request as rq
from gourmet.services.auth_service import AuthService

auth_bp = Blueprint("gourmet_auth", __name__)
auth_service = AuthService()

@auth_bp.route("", methods=["POST"])
def login(): return auth_service.login()
