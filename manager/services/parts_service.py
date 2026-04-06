# Utils
from flask import jsonify, request as rq
from utils.safe_route import safe_route
from utils.db import db
# Models
from manager.models.parts import Part

class PartService:
    @safe_route
    def get(self, token_data) -> tuple:
        cr = token_data.get("cr")
        id_part = rq.args.get("id")
        
        if id_part: 
            part = Part.query.filter_by(id= id_part, cr=cr).first()
            if part: return jsonify(part.to_dict())
            return jsonify("Peça não encontrada!"), 404
        return jsonify([part.to_dict() for part in Part.query.filter_by(cr=cr).all()]), 200
        
    @safe_route
    def create(self, token_data) -> tuple:
        # =========== Vars
        # =========== Banco de Dados
        ...

    @safe_route
    def update(self, token_data) -> tuple:
        # =========== Vars
        # =========== Banco de Dados
        ...
        
    @safe_route
    def delete(self) -> tuple:
        id = rq.args.get("id")
        if id:
            db.session.delete(Part.get(id))
            db.session.commit()
            return jsonify("Peça exclusa com sucesso"), 200
        return jsonify("ID Obrigatorio"), 400


    