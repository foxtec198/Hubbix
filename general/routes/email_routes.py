from flask import Blueprint, request as rq
from general.services.email_service import EmailService

email_bp = Blueprint("Emails", __name__)
email_service = EmailService()

@email_bp.route("/<str:email>", methods=["POST"]) # Envia um email
def main(email):
    match rq.method: 
        case "POST": return email_service.send_mail(email)