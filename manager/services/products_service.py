from manager.models.products import Product, VwProducts
from manager.models.timezone import fuso
from werkzeug.datastructures.headers import Headers
from werkzeug.datastructures.structures import MultiDict
from utils.safe_route import check_connection, require_cr
from utils.now import now
from flask import jsonify, request as rq
from utils.check_field import check_field
from os import path, getcwd
from utils.db import db

class ProductService:
    # @check_connection
    @require_cr
    def get(self, bd:MultiDict, hd:Headers, cr = None): # Obtem todos os produtos
        id = bd.get("id")
        ean = bd.get("ean")
        nome = bd.get("nome")
        if id: return VwProducts._search_by_id(id)
        elif ean: return VwProducts._search_by_ean(ean)
        elif nome: return VwProducts._search_by_name(nome)
        else: return VwProducts._searh_by_cr(cr)

    @check_connection
    @require_cr
    def create(self, bd:MultiDict, hd:Headers, cr = None): # Cria um produto
        files = rq.files # Seta as files da requisição
        nome = bd.get("nome")
        custo = bd.get("custo")
        valor = bd.get("valor")
        estoque_minimo = bd.get("estoque_minimo", 0)
        quantidade = bd.get("quantidade")
        desconto = bd.get("desconto")
        lucro = bd.get("lucro")
        fornecedor = bd.get("fornecedor")
        gc = hd.get("gc")

        ok, error = check_field(
            nome=nome, custo=custo, valor=valor,
            quantidade=quantidade, desconto=desconto,
            lucro=lucro, fornecedor=fornecedor, 
            estoque_minimo=estoque_minimo               
        )

        if ok:
            data = now(fuso(cr)) # Define a data atuaal 
            prod = Product() # Cria o Modelo Produto

            # Seta os valores
            prod.nome = nome
            prod.custo = custo
            prod.valor = valor
            prod.estoque_minimo = estoque_minimo
            prod.quantidade = quantidade
            prod.desconto = desconto
            prod.lucro = lucro
            prod.fornecedor = fornecedor
            prod.data = data
            prod.grupodecliente = gc
            prod.cr = cr

            # Define o Filename
            if files:
                img = files.get('img_file')
                filename = f'prod_{prod.id}.png'
                filepath = path.join(getcwd(), "manager", "assets", "img", "produtos", filename)
                img.save(filepath)
            else: filename = 'blank.png'

            ean = bd.get("ean", prod.id) # Define o EAN

            # Seta o EANe a IMG
            prod.ean = ean
            prod.img = filename
            db.session.add(prod)
            db.session.commit()
            return jsonify({
                "msg": "Produto cadastrado com sucesso",
                "id": prod.id
            }), 200
        return jsonify(error), 400

    @check_connection
    @require_cr
    def update(self, bd:MultiDict, hd:Headers, cr = None):
        files = rq.files # Seta as files da requisição
        id = bd.get("id")
        if id:
            ean = db.get("ean")
            nome = db.get("nome")
            custo = db.get("custo")
            valor = db.get("vaor")
            estoque_minimo = db.get("estoque_minimo")
            quantidade = db.get("quantidade")
            desconto = db.get("desconto")
            lucro = db.get("lucro")
            fornecedor = db.get("fornecedor")
            
            prod = Product.query.filter_by(id=id).one()
            if prod:
                if ean: prod.ean = ean
                if nome: prod.nome = nome
                if custo: prod.custo = custo
                if valor: prod.valor = valor
                if estoque_minimo: prod.estoque_minimo = estoque_minimo
                if quantidade: prod.quantidade = quantidade
                if desconto: prod.desconto = desconto
                if lucro: prod.lucro = lucro
                if fornecedor: prod.fornecedor = fornecedor
                if files:
                    img = files.get('img_file')
                    filename = f'prod_{prod.id}.png'
                    filepath = path.join(getcwd(), "manager", "assets", "img", "produtos", filename)
                    img.save(filepath)
                else: filename = False
                if filename: prod.img = filename
                db.session.commit()
                return jsonify("Atualizado com sucesso!")
            return jsonify("Produto não encontrado!"), 401
        return jsonify("ID Obrigat´roio!"), 400

    @check_connection
    @require_cr
    def delete(self, bd:MultiDict, hd:Headers, cr = None):
        id = bd.get("id")
        if id:
            db.session.delete(Product.query.get(id))
            db.session.commit()
            return jsonify("Exluso com sucesso"), 200
        return jsonify("ID Obrigatório"), 400
    
