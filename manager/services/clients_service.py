# Utils
from werkzeug.datastructures.structures import MultiDict
from werkzeug.datastructures.headers import Headers
from utils.safe_route import check_connection, require_cr
from random import randint
from flask import jsonify
from utils.now import now
# Models
from manager.models.clients import Client, db

class ClientService:
    @check_connection
    @require_cr
    def get(self, bd:MultiDict, hd:Headers, cr = None):
        id = bd.get("client_id", False) # Confirma se tem ID do Cliente
        if id: return jsonify([c.to_dict() for c in Client.query.filter_by(id=id).all()])  # Se tiver o id filtra pelo mesmo
        return jsonify([c.to_dict() for c in Client.query.filter_by(cr=cr).all()])# Aqui separa apenas por CR 
        
    @check_connection
    @require_cr
    def create(self, bd:MultiDict, hd:Headers, cr = None):
        # Credenciais
        gc = hd.get("gc")

        # Dados pessoais
        cpf = bd.get("cpf", 0) # Como não é obrigatorio o CPF ele seta como 0
        nome = bd.get("nome")
        tel = bd.get("tel")
        end = bd.get("end")
        obs = bd.get("obs")
        
        # Aparelho
        modelo = bd.get("modelo")
        marca = bd.get("marca")
        cor = bd.get("cor")
        imei = bd.get("imei")
        
        if nome and tel and modelo and marca and cor: # Dados origatorios
            if cpf == 0: # Em caso da não inserção do CPF consta a geração do CPFF - Exemplo: F_123456789101112
                for i in range(5): # Aqui ele gera um CPFF aleatorio e testa pra confirmar se ja tem igual no BD - 5 tentativas
                    l = 14 # Numero de letras que tera o CPFF que no caso é Ficticio pois o cliente nao desejou informa-lo!
                    newcpf = f"F_{randint(int('0'*l), int('9'*l))}{i}"
                    cpf = Client.query.filter_by(cpf=newcpf).all()
                    if not cpf: 
                        cpf = newcpf
                        break
                    else: return jsonify("Todos CPFF's foram gerados e nenhum livre tente novamente!"), 401
            new = Client()
            new.nome = nome
            new.cpf = cpf
            new.telefone = tel
            new.modelo = modelo
            new.marca = marca
            new.cor = cor
            new.endereco = end
            new.imei = imei
            new.obs = obs
            new.data = now()
            new.grupodecliente = gc
            new.cr = cr
            db.session.add(new)
            db.session.commit()
            return jsonify({
                "status": "ok", 
                "mensagem": "Cliente Cadastrado com sucesso",
                "client_id": new.id
            }), 200
        return jsonify("Confira os dados obrigatórios!"), 400

    @check_connection
    @require_cr
    def update(self, bd:MultiDict, hd:Headers, cr = None):
            # Credenciais
            gc = hd.get("gc")

            # Dados pessoais
            id = bd.get("id", None) # Client id obrigatorio!!!!
            cpf = bd.get("cpf", False)
            nome = bd.get("nome", False)
            telefone = bd.get("tel", False)
            endereco = bd.get("end", False)
            obs = bd.get("obs", False)

            # Dados do aparelho
            modelo = bd.get("modelo", False)
            marca = bd.get("marca", False)
            cor = bd.get("cor", False)
            imei = bd.get("imei", False)

            if id:
                client = Client.query.get(id)
                if cpf: client.cpf = cpf # type: ignore
                if nome: client.nome = nome # type: ignore
                if telefone: client.telefone = telefone # type: ignore
                if endereco: client.endereco = endereco # type: ignore
                if obs: client.obs = obs # type: ignore
                if modelo: client.modelo = modelo # type: ignore
                if marca: client.marca = marca # type: ignore
                if cor: client.cor = cor # type: ignore
                if obs: client.obs = obs # type: ignore
                db.session.commit()
                return jsonify({
                    "status": "ok",
                    "mensagem": "Cliente atualizado com sucesso",
                })
            return jsonify("ID Obirgatório!"), 400
    
    @check_connection
    @require_cr
    def delete(self, bd:MultiDict, hd:Headers, cr = None):
        client_id = bd.get("client_id", None)
        if client_id:
            db.session.delete(Client.query.filter_by(id=client_id, cr=cr))
            db.session.commit()
            return jsonify("Cliente excluso com sucesso!"), 200
        return jsonify("Id Obrigatório"), 400
