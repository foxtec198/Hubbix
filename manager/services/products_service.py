# utils
from manager.models.timezone import fuso
from utils.safe_route import safe_route
from utils.now import now
from flask import jsonify, request as rq
from utils.check_field import check_field
from os import path, getcwd

# models
from manager.models.products import Product, VwProducts, db
from manager.models.categories import Categorie

class ProductService:
    @safe_route
    def get(self, token_data): # Obtem todos os produtos
        args = rq.args
        cr = token_data.get("cr")
        id = args.get("id")
        ean = args.get("ean")
        nome = args.get("nome")

        if id: return VwProducts._search_by_id(id)
        elif ean: return VwProducts._search_by_ean(ean)
        elif nome: return VwProducts._search_by_name(nome)
        else: return VwProducts._searh_by_cr(cr)

    @safe_route
    def get_categories(self, token_data):
        cr = token_data.get('cr')
        categories =  Categorie._search_by_cr(cr)
        categories_map = {c['id']:c["nome"] for c in categories}
        group = {c["nome"]: [] for c in categories}
        products = Product._search_by_cr(cr)

        for product in products:
            nome = categories_map.get(product["id_categoria"])
            if nome: group[nome].append(product)
        
        return jsonify(group)


    @safe_route
    def create(self, token_data): # Cria um produto

        body = rq.form
        files = rq.files # Seta as files da requisição
        cr = token_data.get("cr")
        gc = token_data.get("gc")

        nome = body.get("nome")
        custo = body.get("custo")
        valor = body.get("valor")
        estoque_minimo = body.get("estoque_minimo", 0)
        quantidade = body.get("quantidade")
        desconto = body.get("desconto")
        lucro = body.get("lucro")
        fornecedor = body.get("fornecedor")

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

            ean = body.get("ean", prod.id) # Define o EAN

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

    @safe_route
    def update(self, token_data):
        body = rq.form
        cr = token_data.get("cr")

        files = rq.files # Seta as files da requisição
        id = body.get("id")
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
            
            prod = Product.query.filter_by(id=id, cr=cr).one()
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

    @safe_route
    def delete(self):
        id = rq.args.get("id")
        if id:
            db.session.delete(Product.query.get(id))
            db.session.commit()
            return jsonify("Exluso com sucesso"), 200
        return jsonify("ID Obrigatório"), 400
    