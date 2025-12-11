from werkzeug.datastructures import MultiDict, Headers
from manager.models.parts import Part
from flask import jsonify
from utils.safe_route import require_cr, check_connection
from utils.db import db

class PartService:
    @check_connection
    @require_cr
    def get(self, bd:MultiDict, hd:Headers, cr=None) -> tuple:
        id_part = bd.get("id")
        if id_part: 
            part = Part.query.filter_by(id= id_part, cr=cr).first()
            if part: return jsonify(part.to_dict())
            return jsonify("Peça não encontrada!"), 404
        return jsonify([part.to_dict() for part in Part.query.filter_by(cr=cr).all()]), 200
        
    @check_connection
    @require_cr
    def create(self, bd:MultiDict, hd:Headers, cr=None) -> tuple:
        # =========== Vars
        # =========== Banco de Dados
        ...

    @check_connection
    @require_cr
    def update(self, bd:MultiDict, hd:Headers, cr=None) -> tuple:
        # =========== Vars
        # =========== Banco de Dados
        ...
        
    @check_connection
    @require_cr
    def delete(self, bd:MultiDict, hd:Headers, cr=None) -> tuple:
        id = bd.get("id")
        if id:
            db.session.delete(Part.get(id))
            db.session.commit()
            return jsonify("Peça exclusa com sucesso"), 200
        return jsonify("ID Obrigatorio"), 400


    