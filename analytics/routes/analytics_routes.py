from flask import Blueprint, request as rq, jsonify
from analytics.services.analytics_service import AnalyticService

analytics_bp = Blueprint("Analytics", __name__)
analytics_service = AnalyticService()

@analytics_bp.route("/", methods=["GET", "POST"])
def main():
    match rq.method:
        case "GET": return analytics_service.get(rq.args, rq.headers)
        case "POST": return analytics_service.set(rq.get_json(), rq.headers)
    return jsonify("Metodo nao permitido"), 405


@analytics_bp.route("/login", methods=["POST"])
def login():
    if rq.method == "POST": return analytics_service.login(rq.get_json(), rq.headers)
    return jsonify("Metodo nao permitido"), 405