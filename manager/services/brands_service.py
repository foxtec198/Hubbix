# Utils
from werkzeug.datastructures.structures import MultiDict
from werkzeug.datastructures.headers import Headers
from flask import jsonify
from utils.check_cr import check_cr
from utils.safe_route import check_connection
# Models
from manager.models.brands import Brand, db

class BrandService:
    @check_connection
    def get(self, bd:MultiDict, hd:Headers):
        cr = hd.get("cr", False)
        if check_cr(cr): return jsonify(Brand.search_by_cr(cr))
        return jsonify("Loja Inexistente"), 401
    
    @check_connection
    def create(self, bd:MultiDict, hd:Headers):
        cr = hd.get("cr", False) # Pega o CR
        if check_cr(cr): # Confere o CR
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
                })
            return jsonify("Nome obrigatório"), 400
        return jsonify("Loja inexistente"), 401
    
    @check_connection
    def update(self, bd:MultiDict, hd:Headers):
        cr = hd.get("cr", False) # Pega o CR
        if check_cr(cr): # Confere o CR
            id = bd.get("id")
            brand = Brand.query.filter_by(id=id, cr=cr).one()
            nome = bd.get("nome", "")
            if nome: brand.nome = nome
            db.session.commit()
            return jsonify({
                "msg": "Atualizado com sucesso",
                "ok": False
            }), 401
        return jsonify("Loja Inexistente"), 401
    
    @check_connection
    def delete(self, bd:MultiDict, hd:Headers):
        cr = hd.get("cr", False) # Pega o CR
        if check_cr(cr): # Confere o CR
            id = bd.get("id")
            brand = Brand.query.filter_by(cr=cr, id=id)
            if brand:
                db.session.delete(brand)
                db.session.commit()
                return jsonify({
                    "msg": "Removido com sucesso",
                    "ok": True
                })
            return jsonify("Marca não encontrada"), 400
        return jsonify("Loja Inexistente"), 401
    