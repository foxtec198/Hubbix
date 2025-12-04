# Utils
from werkzeug.datastructures.structures import MultiDict
from werkzeug.datastructures.headers import Headers
from flask import jsonify
from utils.safe_route import check_connection, require_cr
# Models
from manager.models.brands import Brand, db

class BrandService:
    @check_connection
    @require_cr
    def get(self, bd:MultiDict, hd:Headers, cr= None): # Pega todas as marcas por CR
        return jsonify(Brand.search_by_cr(cr))
    
    @check_connection
    @require_cr
    def create(self, bd:MultiDict, hd:Headers, cr = None): # Cria uma marca por CR
        name = bd.get("nome") 
        brand = Brand()
        if name: # Confirma se foi passado o nome
            brand.nome = name
            brand.cr = cr
            db.session.add(brand)
            db.session.commit()
            return jsonify({
                "msg": f"{brand.nome} criada com sucesso!",
                "ok": True,
                "id": brand.id
            }), 201
        return jsonify("Nome obrigatório"), 400
    
    @require_cr
    @check_connection
    def update(self, bd:MultiDict, hd:Headers, cr = None): # Atualiza o nome de uma marca por ID
        id = bd.get("id")
        if id: 
            brand = Brand.query.filter_by(id=id, cr=cr).one()
            if brand:
                nome = bd.get("nome", "")
                if nome: brand.nome = nome
                db.session.commit()
                return jsonify({
                    "msg": "Atualizado com sucesso",
                    "ok": False
                }), 401
            return jsonify("Marca não encontrada"), 400
        return jsonify("ID Obrigatorio"), 400
    
    @require_cr
    @check_connection
    def delete(self, bd:MultiDict, hd:Headers, cr = None): # DEleta uma marca especfica por ID
        id = bd.get("id")
        if id:
            brand = Brand.query.get(id)
            if brand:
                db.session.delete(brand)
                db.session.commit()
                return jsonify({
                    "msg": "Removido com sucesso",
                    "ok": True
                })
            return jsonify("Marca não encontrada"), 400
        return jsonify("ID Obrigatorio"), 400
    