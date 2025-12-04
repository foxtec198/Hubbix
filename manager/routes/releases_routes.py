from manager.services.releases_service import ReleaseService
from flask import Blueprint, request, jsonify

release_bp = Blueprint("Saidas", __name__)
release_service = ReleaseService()

@release_bp.route("/", methods=["GET", "POST", "PATCH", "DELETE"])
def main():
    ...