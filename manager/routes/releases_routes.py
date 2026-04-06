from manager.services.releases_service import ReleaseService
from flask import Blueprint, request as rq, jsonify

release_bp = Blueprint("Saidas", __name__)
release_service = ReleaseService()

@release_bp.route("/", methods=["GET", "POST", "PATCH", "DELETE"])
def main():
    match rq.method:
        case "GET": return release_service.get_releases()
        case "DELETE": return release_service.delete_release()