from werkzeug.datastructures import MultiDict, Headers
from manager.models.providers import Provider
from utils.safe_route import require_cr, check_connection
from utils.db import db
from flask import jsonify

class ProviderService:
    @check_connection
    @require_cr
    def get(self, bd:MultiDict, hd:Headers, cr=None) -> tuple:
        id = bd.get("id")
        if id:
            provider = Provider.query.filter_by(id=id, cr=cr).first()
            if provider: return jsonify(provider.to_dict()), 200
            else: return jsonify("Fornecedor não encontrado"), 404
        return jsonify([provider.to_dict() for provider in Provider.query.filter_by(cr=cr).all()]), 200
        

    @check_connection
    @require_cr
    def create(self, bd:MultiDict, hd:Headers, cr=None) -> tuple:
        ...

    @check_connection
    @require_cr
    def update(self, bd:MultiDict, hd:Headers, cr=None) -> tuple:
        ...

    @check_connection
    @require_cr
    def delete(self, bd:MultiDict, hd:Headers, cr=None) -> tuple:
        id = bd.get("id")
        if id:
            db.session.delete(Provider.get(id))
            db.session.commit()
            return jsonify("Fornecedor excluso com sucesso"), 200
        return jsonify("ID Obrigatorio"), 400