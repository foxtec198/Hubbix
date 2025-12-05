from werkzeug.datastructures import MultiDict, Headers
from utils.check_field import check_field
from flask import jsonify
from general.models.email import Email
from threading import Thread

class EmailService:
    def send_mail(self, bd:MultiDict, hd:Headers, email): # Envio de email "Generico"
        html = bd.get("html")
        body = bd.get("body")
        title = bd.get("title")

        ok, error = check_field(
            html=html, 
            body=body, 
            title=title, 
            email=email
        )

        if ok:
            try:
                Thread(target=Email().send, args=(title, html, email)).start()
                return jsonify("Email sendo enviado"), 201
            except Exception as err: return jsonify("Erro ao enviar o email: " + err), 500
        return jsonify(error), 400

