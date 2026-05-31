from flask import Blueprint, request as rq
from gourmet.services.pos_service import POSService

pos_bp = Blueprint("gourmet_pos", __name__)
pos_service = POSService()

@pos_bp.route("", methods=["GET", "POST", "PATCH", "DELETE"])
def pos():
    match rq.method:
        case "GET": return pos_service.check(token_data=rq.headers)
        case "POST": return pos_service.open(token_data=rq.headers)
        case "PATCH": return pos_service.apply(token_data=rq.headers)
        case "DELETE": return pos_service.close(token_data=rq.headers)

@pos_bp.route("/last_value", methods=["GET"])
def last_value():
    return pos_service.last_value(token_data=rq.headers)
