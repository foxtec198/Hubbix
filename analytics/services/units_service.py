from werkzeug.datastructures import MultiDict, Headers
from flask import jsonify
from analytics.models.units import Unit
from utils.db import db

class UnitService:
    def get(self, bd:MultiDict, hd:Headers):
        unit_id = hd.get("unit_id")
        if unit_id: 
            unit = Unit.query.filter_by(id=unit_id).first()
            if unit: return jsonify(unit.to_dict())
        return jsonify([u.to_dict() for u in Unit.query.all()])

    def create_unit(self, bd:MultiDict, hd:Headers):
        name = bd.get("nome")
        if name:
            unit = Unit(name=name)
            db.session.add(unit)
            db.session.commit()
            return jsonify({"msg":"Criado com sucesso", "id": unit.id}), 201
        return jsonify("Nome Obrigatorio"), 400
        