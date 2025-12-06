from werkzeug.datastructures import MultiDict, Headers
from flask import jsonify
from analytics.models.user import User
from hashlib import sha256
from utils.db import db

class UserService:
    def create_user(self, bd:MultiDict, hd:Headers):
        name = bd.get("nome")
        email = bd.get("email")
        pwd = bd.get("pwd")
        unit_id = bd.get("unit_id")

        need = ['name', 'email', 'pwd', 'unit_id'] # Dados obrigatorios
        falt = [campo for campo in need if not locals()[campo]] # Confere se falta algum
        
        if not falt:
            user = User()
            user.name = name
            user.email = email
            user.unit_id = unit_id
            db.session.add(user)
            db.session.commit()
            user.hash = sha256(pwd.encode()).hexdigest()
        return jsonify(f"Faltando: {falt}"), 400

    def delete_user(self, bd:MultiDict, hd:Headers):
        id = bd.get("id")
        db.session.delete(User.query.get(id))
        return jsonify("Excluso com sucesso"), 200