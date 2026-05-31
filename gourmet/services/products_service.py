from flask import jsonify, request as rq
from utils.safe_route import safe_route
from utils.now import now
from gourmet.models.products import Product
from gourmet.models.categories import Category
from gourmet.models.config import Config
from utils.db import db
from os import path, getcwd

class ProductService:
    @safe_route
    def get(self, token_data):
        cr = token_data.get('cr')
        args = rq.args
        id = args.get('id')
        nome = args.get('nome')

        if id:
            return Product._search_by_id(id)
        elif nome:
            return jsonify(Product._search_by_nome(nome)), 200
        else:
            return jsonify(Product._search_by_cr(cr)), 200

    @safe_route
    def create(self, token_data):
        cr = token_data.get('cr')
        gc = token_data.get('gc')
        data = rq.form
        files = rq.files

        nome = data.get('nome')
        categoria = data.get('categoria')
        custo = data.get('custo')
        valor = data.get('valor')
        quantidade = data.get('quantidade')
        alerta = data.get('alerta')
        preparo = data.get('preparo') == 'on'
        sku = data.get('sku')

        if not all([nome, categoria, custo, valor, quantidade]):
            return jsonify({'error': 'Campos obrigatórios faltando'}), 400

        prod = Product(
            nome=nome.upper(),
            id_categoria=categoria,
            custo=float(custo),
            valor=float(valor),
            quantidade=int(quantidade),
            alerta=alerta,
            preparo=preparo,
            cr=cr,
            grupodecliente=gc
        )

        db.session.add(prod)
        db.session.flush()

        if files and 'img' in files:
            img = files['img']
            filename = f'prod_{prod.id}.png'
            filepath = path.join(getcwd(), 'gourmet', 'assets', 'img', 'produtos', filename)
            img.save(filepath)
            prod.img = filename

        prod.sku = sku if sku else prod.id
        db.session.commit()

        return jsonify({'msg': 'Produto cadastrado com sucesso', 'id': prod.id}), 200

    @safe_route
    def update(self, token_data):
        cr = token_data.get('cr')
        data = rq.form
        files = rq.files
        id = data.get('id')

        if not id:
            return jsonify({'error': 'ID obrigatório'}), 400

        prod = Product._search_by_id(id)
        if not prod:
            return jsonify({'error': 'Produto não encontrado'}), 404

        if prod.cr != cr:
            return jsonify({'error': 'Acesso negado'}), 403

        if data.get('nome'):
            prod.nome = data.get('nome')
        if data.get('categoria'):
            prod.id_categoria = data.get('categoria')
        if data.get('custo'):
            prod.custo = float(data.get('custo'))
        if data.get('valor'):
            prod.valor = float(data.get('valor'))
        if data.get('quantidade'):
            prod.quantidade = int(data.get('quantidade'))
        if data.get('alerta'):
            prod.alerta = data.get('alerta')
        if data.get('sku'):
            prod.sku = data.get('sku')
        if data.get('preparo'):
            prod.preparo = data.get('preparo') == 'on'

        if files and 'img' in files:
            img = files['img']
            filename = f'prod_{prod.id}.png'
            filepath = path.join(getcwd(), 'gourmet', 'assets', 'img', 'produtos', filename)
            img.save(filepath)
            prod.img = filename

        db.session.commit()
        return jsonify({'msg': 'Produto atualizado com sucesso'}), 200

    @safe_route
    def delete(self, token_data):
        cr = token_data.get('cr')
        data = rq.get_json()
        id = data.get('id')

        if not id:
            return jsonify({'error': 'ID obrigatório'}), 400

        prod = Product._search_by_id(id)
        if not prod:
            return jsonify({'error': 'Produto não encontrado'}), 404

        if prod.cr != cr:
            return jsonify({'error': 'Acesso negado'}), 403

        db.session.delete(prod)
        db.session.commit()
        return jsonify({'msg': 'Produto deletado com sucesso'}), 200
