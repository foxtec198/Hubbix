from werkzeug.datastructures import MultiDict, Headers
from analytics.models.clients import Client
from flask import jsonify
from utils.db import db

class ClientService:
    def get(self, bd:MultiDict, hd:Headers):
        id = hd.get("id")
        if id: return jsonify([c.to_dict() for c in Client.query.filter_by(unit_id=id).all()])
        return jsonify("Unit Id obrigatorio")

    def create_client(self, bd:MultiDict, hd:Headers):
        name = bd.get("nome")
        link = bd.get("link")
        unit_id = hd.get("unit_id")
        
        need = ["name", "unit_id"]
        falt = [camp for camp in need if not locals()[camp]]

        if not falt:
            client = Client()
            client.name = name
            client.unit_id = unit_id
            client.link = link
            db.session.add(client)
            db.session.commit()
            return jsonify({'status': True, 'id': client.id}), 200
        return jsonify(f"Dados faltando: {falt}"), 400
        
    def update_client(self, bd:MultiDict, hd:Headers):
        client_id = bd.get("id")
        name = bd.get("nome")
        link = bd.get("link")
        
        client = Client.query.filter_by(id=client_id).first()
        if client:
            if name: client.name = name
            if link: client.link = link
            db.session.commit()
            return jsonify("Alterado com sucesso"), 200
        return jsonify("Cliente nao encontrado"), 404
    
    def delete_client(self, bd:MultiDict, hd:Headers):
        unit_id = hd.get("unit_id")
        client_id = bd.get("id")

        need = ["unit_id", "client_id"]
        falt = [camp for camp in need if not locals()[camp]]

        if not falt:
            db.session.delete(Client.query.get(client_id))
            db.session.commit()
            return jsonify("Excluso com sucesso"), 200
        return jsonify(f"Faltando: {falt}"), 400