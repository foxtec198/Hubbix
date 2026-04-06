from utils.check_field import check_field
from flask import jsonify, request as rq
from general.models.email import Email
from threading import Thread

class EmailService:
    def send_mail(self, email): # Envio de email "Generico"
        body = rq.get_json()
        html = body.get("html")
        body = body.get("body")
        title = body.get("title")

        ok, error = check_field(
            html=html, body=body, 
            title=title, email=email
        )

        if ok:
            try:
                Thread(target=Email().send, args=(title, html, email)).start()
                return jsonify("Email sendo enviado"), 200 # Retorna 200 - OK
            except Exception as err: return jsonify("Erro ao enviar o email: " + err), 500 # Retorna 500 - Server Error
        return jsonify(error), 400 # Retorna 400 - BAD REQUEST

