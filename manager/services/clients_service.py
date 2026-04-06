# Utils
from random import randint
from flask import jsonify, request as rq
from utils.safe_route import safe_route
from utils.check_field import check_field
from utils.now import now
from manager.models.timezone import fuso
# Models
from manager.models.clients import Client, db

class ClientService:
    @safe_route
    def get(self, token_data) -> tuple:
        """
        Docstring for get
        
        :param bd: Body(Argumentos) passado opcionalemnte
        :type bd: MultiDict
        :param cr: Credecial de Loja passado no Header por obrigatório (Não declarar na função)
        :return: (JSON, CODE)
        :rtype: tuple[Response, Literal[404]] | tuple[Response, Literal[200]]
        """

        cr = token_data.get("cr")
        id = rq.args.get("client_id") # Confirma se tem ID do Cliente
        if id: # Confirma se o ID foi declardo
            client = Client.get_client(cr, id) # Busca o cliente por ID e Loja
            if client: return jsonify(client.to_dict()), 200# Se o ID for declarado filtra pelo mesmo
            return jsonify("Cliente não localizado"), 404 # Retorna NOT FOUND - 404
        return jsonify(Client._search_by_cr(cr)), 200 # Retorna os clientes por CR 
        
    @safe_route
    def create(self, token_data):
        """
        ### Docstring for create client.

        :rtype: tuple[Response, Literal[201]] | tuple[Response, Literal[400]]
        """

        body = rq.get_json()
        cr = token_data.get("cr")
        gc = token_data.get("gc")

        # ============= Dados do Cliente
        cpf = body.get("cpf", 0) # Caso não seja declarado o CPF seta o valor como 0(Zero)
        name = body.get("nome") # Nome do Cliente
        tel = body.get("tel") # Telefone do Cliente
        address = body.get("end") # Endereço do Cliente
        obs = body.get("obs") # Observação do cliente - IMPORTANTE: Coloque apenas se for algo NEGATIVO!
        
        # ============= Dados do aparelho
        model = body.get("modelo") # Modelo Ex:  G82, Note 10, A13
        brand = body.get("marca") # Marca Ex: Samsumg, Xiaomi, Motorola
        color = body.get("cor") # Cor Ex: Branco, Preto, Rosa
        imei = body.get("imei") # IMEI de Identificação do Aparelho importante porém opcional

        # Checka se foram declarados os dados obrigatórios
        ok,error = check_field(
            nome=name, telefone=tel, 
            modelo=model, marca=brand, 
            cor=color
        )
        
        if ok: # Confere se os dados obrigatorios estão OK
            if cpf == 0: # Em caso da não inserção do CPF consta a geração do CPFF(CPF FAKE) - Exemplo: F_123456789101112
                l = 14 # Numero de letras que terá o CPFF que no caso é Ficticio pois o cliente nao desejou informa-lo!
                i = 1 # Numero de tentativas até liberar o CPFF
                cpfF = f"F_{randint(int('0'*l), int('9'*l))}{i}" # Gera uma vez
                while Client._search_by_cpf(cr, cpfF): 
                    i += 1
                    cpfF = f"F_{randint(int('0'*l), int('9'*l))}{i}"
                cpf = cpfF # Assim que encontrar um CPFF adiciona ao CPF antigo setado como 0(Zero)

            client = Client( # Cria um cliente e seta todos os dados passados!
                nome =name, cpf = cpf,
                telefone = tel, modelo = model,
                marca = brand, cor = color,
                endereco = address,
                imei = imei, obs = obs,
                data = now(fuso(cr)),
                grupodecliente = gc, cr = cr
            )
            db.session.add(client) # Adiciona ao Banco de Dados 
            db.session.commit() # Salva no Banco de Dados
            return jsonify({ "mensagem": "Cliente cadastrado", "client_id": client.id }), 201 # Retorna Sucesso com o ID do cliente
        return jsonify(f"Falta alguns dados - {error}"), 400 # Retorna BAD REQUEST - 400

    @safe_route
    def update(self, token_data):
        """
        Docstring for update
        
        :param bd: Body(JSON) passado com os dados a serem utilizados
        :type bd: MultiDict
        :param cr: Credecial de Loja passado no Header por obrigatório (Não declarar na função)
        :return: (JSON, CODE)
        :rtype: tuple[Response, Literal[200]] | tuple[Response, Literal[404]] | tuple[Response, Literal[400]]

        OBS: Para mais duvidas consulte a doc da API
        """

        body = rq.get_json() # Body passado em JSON
        cr = token_data.get("cr")

        # ============= Dados do Cliente
        id = body.get("id") # ID de Cliente é obrigatorio!!!!
        cpf = body.get("cpf") # CPF
        nome = body.get("nome") # Nome
        tel = body.get("tel") # Telefone
        address = body.get("end") # Endereço
        obs = body.get("obs") # OBS - IMPORTANTE: Só adicione uma OBS caso ela seja NEGATIVA!

        # ============= Dados do aparelho
        modelo = body.get("modelo")
        marca = body.get("marca")
        cor = body.get("cor")
        imei = body.get("imei")

        if id:
            client = Client.get_client(cr, id) # Obtem o cliente por Loja e por id
            if client: # Altera cada um dos dados caso tenham sido passado, caso contrario ignora!
                if cpf: client.cpf = cpf
                if nome: client.nome = nome
                if tel: client.telefone = tel
                if address: client.endereco = address
                if obs: client.obs = obs
                if modelo: client.modelo = modelo
                if marca: client.marca = marca
                if cor: client.cor = cor
                if obs: client.obs = obs
                if imei: client.imei = imei
                db.session.commit() # Salva os dados no Banco
                return jsonify("Cliente atualizado"), 200 # Retorna Sucesso
            return jsonify("Cliente não encontrado"), 404 # Retorna NOT FOUND - 404
        return jsonify("Id obrigatorio"), 400 # Retorna BAD REQUEST - 400

    @safe_route
    def delete(self):
        """
        ### Docstring for delete client.
        :rtype: tuple[Response, Literal[200]] | tuple[Response, Literal[400]]
        """

        client_id = rq.args.get("client_id") # Busca o id do cliente
        if client_id: # Confirma se foi declarado o ID
            db.session.delete(Client.query.get(client_id)) # Remove o cliente por id
            db.session.commit() # Salva os dados no banco
            return jsonify("Cliente removido"), 200 # Retorna Sucesso
        return jsonify("Id Obrigatório"), 400 # Retorna BAD REQUEST - 400