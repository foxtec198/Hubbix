# Utils
from manager.models.brands import Brand, db
from flask import jsonify, request as rq
from utils.safe_route import safe_route

class BrandsService:
    @safe_route
    def get(self, token_data) -> tuple:
        """
        Docstring for get
        
        :param bd: Body(Argumentos) passado com ID (não Obrigatorio)
        :type bd: MultiDict
        :param cr: Credencial da Loja passada no Header (Não declarar na função)
        :return: (JSON, CODE)
        :rtype: tuple[Response, Literal[404]] | tuple[Response, Literal[200]]
        """
        cr = token_data.get("cr") # Obtém o CR do token
        id = rq.args.get("id") # Busca o id da Marca
        if id: # Confere se foi declardao o id
            brand = Brand.get_brand(cr, id) # Pega a marca por ID
            if brand: return jsonify(brand.to_dict()), 200 # Retorna os dados da marca por id
            return jsonify("Marca não encontrada"), 404 # Retorna NOT FOUND - 404
        return jsonify(Brand._search_by_cr(cr)), 200 # Retorna as marcas por loja, caso nao declarado o id
    
    @safe_route
    def create(self, token_data) -> tuple: 
        """
        Docstring for create
        
        :param bd: Body(JSON) passado para que seja feita a criação
        :type bd: MultiDict
        :param cr: Credencial da Loja passada no Header (Não declarar na função)
        :return: (JSON, CODE)
        :rtype: tuple[Response, Literal[400]] | tuple[Response, Literal[201]]
        """
        cr = token_data.get("cr") # Obtém o CR do Token
        body = rq.get_json() # Obtem o JSON do Body
        name = body.get("nome") # Nome da Marca

        if name: # Confirma se foi passado o nome
            brand = Brand(nome= name, cr= cr) # Cria o registro no Banco de Dados
            db.session.add(brand) # Adiciona o registro
            db.session.commit() # Salva os dados
            return jsonify({ "msg": f"{brand.nome} criada com sucesso!", "id": brand.id }), 201 # Retorna CREATED, com o id da marca
        return jsonify("Nome obrigatório"), 400 # Retorna BAD REQUEST - Caso falte algum dado obrigatorio
    
    @safe_route
    def update(self, token_data) -> tuple: 
        """
        Docstring for update
        
        :param bd: Body(JSON) passado para fazer atualização
        :type bd: MultiDict
        :param cr: Credencial da Loja passada no Header (Não declarar na função)
        :return: (JSON, CODE)
        :rtype: tuple[Response, Literal[404]] | tuple[Response, Literal[200]] | tuple[Response, Literal[400]]
        """
        cr = token_data.get("cr") # Obtém o CR do Token
        
        body = rq.get_json() # Obtem o JSON do Body
        id = body.get("id") # Busca o id da marca a ser alterada
        nome = body.get("nome") # Nome a ser alterado

        if id: # Confere se o id foi declarado
            brand = Brand.get_brand(cr, id) # Busca a marca por ID e Loja
            if brand: # Caso seja encontrado
                if nome: brand.nome = nome # Altera caso tenha sido declarado o nome
                db.session.commit() # Salva os dados no Banco
                return jsonify("Marca Atualizada"), 200 # Retorna sucesso
            return jsonify("Marca não encontrada"), 404 # Retorna NOT FOUND - 404
        return jsonify("ID Obrigatorio"), 400 # Retorna BAD REQUEST - 400
    
    @safe_route
    def delete(self) -> tuple: 
        """
        Docstring for delete
        
        :param bd: Body(Argumentos) que deve ser passado o ID da marca (Obrigatorio)
        :type bd: MultiDict
        :param cr: Credencial da Loja passada no Header (Não declarar na função)
        :return: (JSON, CODE)
        :rtype: tuple[Response, Literal[200]] | tuple[Response, Literal[400]]
        """

        id = rq.args.get("id") # Busca o ID da MArca
        if id: # Confere se o id foi declarado
            db.session.delete(Brand.query.get(id)) # Deleta a marca
            db.session.commit() # Salva os dados no Banco
            return jsonify("Marca removida"), 200 # Retorna sucesso
        return jsonify("ID Obrigatorio"), 400 # Retorna BAD REQUEST - 400
    