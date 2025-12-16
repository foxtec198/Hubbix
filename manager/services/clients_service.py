from werkzeug.datastructures import MultiDict, Headers
from utils.safe_route import check_connection, require_cr
from manager.models.clients import Client, db
from manager.models.timezone import fuso
from random import randint
from flask import jsonify
from utils.now import now
from utils.check_field import check_field

class ClientService:
    @check_connection
    @require_cr
    def get(self, bd:MultiDict, cr = None):
        """
        Docstring for get
        
        :param bd: Body(Argumentos) passado opcionalemnte
        :type bd: MultiDict
        :param cr: Credecial de Loja passado no Header por obrigatório (Declare apenas no Header na função não!)
        :return: (JSON, CODE)
        :rtype: tuple[Response, Literal[404]] | tuple[Response, Literal[200]]
        """

        id = bd.get("client_id") # Confirma se tem ID do Cliente
        if id: # Confirma se o ID foi declardo
            client = Client.get_client(cr, id) # Busca o cliente por ID e Loja
            if client: return jsonify(client.to_dict()), 200# Se o ID for declarado filtra pelo mesmo
            return jsonify("Cliente não localizado"), 404 # Retorna NOT FOUND - 404
        return jsonify(Client._search_by_cr(cr)), 200 # Retorna os clientes por CR 
        
    @check_connection
    @require_cr
    def create(self, bd:MultiDict, hd:Headers, cr = None):
        """
        Docstring for create
        
        :param bd: Body(JSON) deve ser passado os dados do Cliente a ser cadastrado
        :type bd: MultiDict
        :param hd: Headers onde deve ser declarado o CR e o GC como obrigatórios
        :type hd: Headers
        :param cr: Credecial de Loja passado no Header por obrigatório (Declare apenas no Header na função não!)
        :return: (JSON, CODE)
        :rtype: tuple[Response, Literal[201]] | tuple[Response, Literal[400]]
        """

        # ============= Dados do Cliente
        cpf = bd.get("cpf", 0) # Caso não seja declarado o CPF seta o valor como 0(Zero)
        name = bd.get("nome") # Nome do Cliente
        tel = bd.get("tel") # Telefone do Cliente
        address = bd.get("end") # Endereço do Cliente
        obs = bd.get("obs") # Observação do cliente - IMPORTANTE: Coloque apenas se for algo NEGATIVO!
        gc = hd.get("gc") # Grupo de Cliente
        
        # ============= Dados do aparelho
        model = bd.get("modelo") # Modelo Ex:  G82, Note 10, A13
        brand = bd.get("marca") # Marca Ex: Samsumg, Xiaomi, Motorola
        color = bd.get("cor") # Cor Ex: Branco, Preto, Rosa
        imei = bd.get("imei") # IMEI de Identificação do Aparelho importante porém opcional

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

    @check_connection
    @require_cr
    def update(self, bd:MultiDict, cr = None):
        """
        Docstring for update
        
        :param bd: Body(JSON) passado com os dados a serem utilizados
        :type bd: MultiDict
        :param cr: Credecial de Loja passado no Header por obrigatório (Declare apenas no Header na função não!)
        :return: (JSON, CODE)
        :rtype: tuple[Response, Literal[200]] | tuple[Response, Literal[404]] | tuple[Response, Literal[400]]

        OBS: Para mais duvidas consulte a doc da API
        """
        # ============= Dados do Cliente
        id = bd.get("id") # ID de Cliente é obrigatorio!!!!
        cpf = bd.get("cpf") # CPF
        nome = bd.get("nome") # Nome
        tel = bd.get("tel") # Telefone
        address = bd.get("end") # Endereço
        obs = bd.get("obs") # OBS - IMPORTANTE: Só adicione uma OBS caso ela seja NEGATIVA!

        # ============= Dados do aparelho
        modelo = bd.get("modelo")
        marca = bd.get("marca")
        cor = bd.get("cor")
        imei = bd.get("imei")

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

    @check_connection
    def delete(self, bd:MultiDict):
        """
        Docstring for delete
        
        :param bd: Body(Argumentos) onde deverá ser passado o ID do cliente (Obrigatorio)
        :type bd: MultiDict
        :return: (JSON, CODE)
        :rtype: tuple[Response, Literal[200]] | tuple[Response, Literal[400]]
        """

        client_id = bd.get("client_id") # Busca o id do cliente
        if client_id: # Confirma se foi declarado o ID
            db.session.delete(Client.query.get(client_id)) # Remove o cliente por id
            db.session.commit() # Salva os dados no banco
            return jsonify("Cliente removido"), 200 # Retorna Sucesso
        return jsonify("Id Obrigatório"), 400 # Retorna BAD REQUEST - 400