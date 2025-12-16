# Utils
from werkzeug.datastructures import MultiDict
from manager.models.brands import Brand, db
from flask import jsonify
from utils.safe_route import check_connection, require_cr

class BrandService:
    @check_connection
    @require_cr
    def get(self, bd:MultiDict, cr= None):
        """
        Docstring for get
        
        :param bd: Body(Argumentos) passado com ID (não Obrigatorio)
        :type bd: MultiDict
        :param cr: Credencial da Loja passada no Header (Não declarar na função)
        :return: (JSON, CODE)
        :rtype: tuple[Response, Literal[404]] | tuple[Response, Literal[200]]
        """
        id = bd.get("id") # Busca o id da Marca
        if id: # Confere se foi declardao o id
            brand = Brand.get_brand(cr, id) # Pega a marca por ID
            if brand: return jsonify(brand.to_dict()), 200 # Retorna os dados da marca por id
            return jsonify("Marca não encontrada"), 404 # Retorna NOT FOUND - 404
        return jsonify(Brand._search_by_cr(cr)), 200 # Retorna as marcas por loja, caso nao declarado o id
    
    @check_connection
    @require_cr
    def create(self, bd:MultiDict, cr = None) -> tuple: 
        """
        Docstring for create
        
        :param bd: Body(JSON) passado para que seja feita a criação
        :type bd: MultiDict
        :param cr: Credencial da Loja passada no Header (Não declarar na função)
        :return: (JSON, CODE)
        :rtype: tuple[Response, Literal[400]] | tuple[Response, Literal[201]]
        """
        name = bd.get("nome") # Nome da Marca
        if name: # Confirma se foi passado o nome
            brand = Brand(nome = name,cr = cr) # Cria o registro no Banco de Dados
            db.session.add(brand) # Adiciona o registro
            db.session.commit() # Salva os dados
            return jsonify({ "msg": f"{brand.nome} criada com sucesso!", "id": brand.id }), 201 # Retorna CREATED, com o id da marca
        return jsonify("Nome obrigatório"), 400 # Retorna BAD REQUEST - Caso falte algum dado obrigatorio
    
    @require_cr
    @check_connection
    def update(self, bd:MultiDict, cr = None) -> tuple: 
        """
        Docstring for update
        
        :param bd: Body(JSON) passado para fazer atualização
        :type bd: MultiDict
        :param cr: Credencial da Loja passada no Header (Não declarar na função)
        :return: (JSON, CODE)
        :rtype: tuple[Response, Literal[404]] | tuple[Response, Literal[200]] | tuple[Response, Literal[400]]
        """
        id = bd.get("id") # Busca o id da marca a ser alterada
        nome = bd.get("nome") # Nome a ser alterado

        if id: # Confere se o id foi declarado
            brand = Brand.get_brand(cr, id) # Busca a marca por ID e Loja
            if brand: # Caso seja encontrado
                if nome: brand.nome = nome # Altera caso tenha sido declarado o nome
                db.session.commit() # Salva os dados no Banco
                return jsonify("Marca Atualizada"), 200 # Retorna sucesso
            return jsonify("Marca não encontrada"), 404 # Retorna NOT FOUND - 404
        return jsonify("ID Obrigatorio"), 400 # Retorna BAD REQUEST - 400
    
    @require_cr
    @check_connection
    def delete(self, bd:MultiDict, cr = None) -> tuple: 
        """
        Docstring for delete
        
        :param bd: Body(Argumentos) que deve ser passado o ID da marca (Obrigatorio)
        :type bd: MultiDict
        :param cr: Credencial da Loja passada no Header (Não declarar na função)
        :return: (JSON, CODE)
        :rtype: tuple[Response, Literal[200]] | tuple[Response, Literal[400]]
        """
        id = bd.get("id") # Busca o ID da MArca
        if id: # Confere se o id foi declarado
            db.session.delete(Brand.query.get(id)) # Deleta a marca
            db.session.commit() # Salva os dados no Banco
            return jsonify("Marca removida"), 200 # Retorna sucesso
        return jsonify("ID Obrigatorio"), 400 # Retorna BAD REQUEST - 400
    