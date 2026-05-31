from flask import jsonify, request as rq
from utils.safe_route import safe_route
from gourmet.models.categories import Category
from utils.db import db

class CategoryService:
    @safe_route
    def get(self, token_data):
        cr = token_data.get('cr')
        if not cr:
            return jsonify({'error': 'CR obrigatório'}), 400

        categories = Category._search_by_cr(cr)
        return jsonify(categories), 200

    @safe_route
    def create(self, token_data):
        cr = token_data.get('cr')
        gc = token_data.get('gc')
        data = rq.get_json()
        nome = data.get('nome')

        if not nome or nome == 'COMBOS':
            return jsonify({'error': 'Nome inválido'}), 400

        category = Category(nome=nome, cr=cr, grupodecliente=gc)
        db.session.add(category)
        db.session.commit()
        return jsonify({'msg': 'Categoria criada com sucesso'}), 200

    @safe_route
    def update(self, token_data):
        cr = token_data.get('cr')
        data = rq.get_json()
        id = data.get('id')
        nome = data.get('nome')

        if not id or not nome:
            return jsonify({'error': 'ID e nome são obrigatórios'}), 400

        category = Category._search_by_id(id)
        if not category or category.cr != cr:
            return jsonify({'error': 'Categoria não encontrada'}), 404

        category.nome = nome
        db.session.commit()
        return jsonify({'msg': 'Categoria atualizada com sucesso'}), 200

    @safe_route
    def delete(self, token_data):
        cr = token_data.get('cr')
        data = rq.get_json()
        id = data.get('id')

        if not id:
            return jsonify({'error': 'ID obrigatório'}), 400

        category = Category._search_by_id(id)
        if not category or category.cr != cr:
            return jsonify({'error': 'Categoria não encontrada'}), 404

        db.session.delete(category)
        db.session.commit()
        return jsonify({'msg': 'Categoria deletada com sucesso'}), 200
