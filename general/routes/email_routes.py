from flask import jsonify, Blueprint, request as rq
from general.services.email_service import EmailService

email_bp = Blueprint("Emails", __name__)
email_service = EmailService()

@email_bp.route("/<email>", methods=["POST"]) # Envia um email
def main(email):
    if rq.method == "POST": return email_service.send_mail(email, rq.get_json(), rq.headers)
    return jsonify("Metodo nao permitido"), 405