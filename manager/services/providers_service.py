from werkzeug.datastructures import MultiDict, Headers
from manager.models.providers import Provider
from utils.safe_route import require_cr, check_connection
from utils.db import db
from flask import jsonify
from utils.check_field import check_field

class ProviderService:
    @check_connection
    @require_cr
    def get(self, bd:MultiDict, cr=None) -> tuple:
        id = bd.get("id")
        if id: # Confirma se foi passado o id no argumentos
            provider = Provider.get_provider(cr, id)
            if provider: # retorna o fornecedor caso exista, se nao retorna NAO ENCONTRADO - 404
                return jsonify(provider.to_dict()), 200 
            return jsonify("Fornecedor não encontrado"), 404
        # Caso não seja passado o id retorna a lista por CR
        return jsonify(Provider._search_by_cr(cr)), 200

    @check_connection
    @require_cr
    def create(self, bd:MultiDict, hd:Headers, cr=None) -> tuple:
        # =============== Dados do Fornecedor e da Loja (CR, GC)
        nome = bd.get("nome") # Nome do Forn.
        telefone = bd.get("telefone") # Telefone do Forn.
        gc = hd.get("gc") # Grupo de Cliente - Passado no Headers
        
        # =============== Conferencias e retorno
        # Confirma os campos obrigatórios 
        # Apenas um campo obrigatório, mas caso necessite de mais, é só adiconar a função
        ok, error = check_field(nome=nome)

        if ok: # Caso todos os dados obrigatórios estiverem presentes
            provider = Provider( # Cria o provider e seta seus dados
                nome = nome,
                telefone = telefone,
                cr = cr,
                grupodecliente = gc
            )
            db.session.add(provider) # Adiciona ao Banco de Dados
            db.session.commit() # Salva as alterações
            # Retorna Sucesso e o ID
            return jsonify({"msg": "Fornecedor criado", "id": provider.id}), 201
        return jsonify(error), 400 # Retorna erro de requisição


    @check_connection
    @require_cr
    def update(self, bd:MultiDict, cr=None) -> tuple:
        # ================= Dados a serem atualizados!!!
        id = bd.get("id") # ID do Fornecedor
        nome = bd.get("nome") # Nome do Fornecedor
        telefone = bd.get("telefone") # Telefone do Fornecedor

        # ================= Conferencias e Retornos
        if id: # ID Obrigatório
            provider = Provider.get_provider(cr, id) # Obtem o fornecedor
            if provider: # Caso exista da a continuidade
                if nome: provider.nome = nome # Atualiza o nome caso seja declarado
                if telefone: provider.telefone = telefone # Atualiza o telefone caso seja declarado
                db.session.commit() # Salva as alterações
                return jsonify("Fornecedor atualizado"), 200 # Retorna Sucesso
            return jsonify("Fornecedor nao encontrado"), 404  # Retorna, NAO ENCONTRADO - 404
        return jsonify("ID Obrigatório"), 400  # Retorna erro de requisição, BAD REQUEST - 400

    @check_connection
    @require_cr
    def delete(self, bd:MultiDict, cr=None) -> tuple:
        id = bd.get("id") # Obtem o id 
        if id: # Confere se foi declarado
            db.session.delete(Provider.get(id)) # Deleta o fornecedor
            db.session.commit() # Salva as altterações
            return jsonify("Fornecedor removido"), 200 # Retorna sucesso 
        return jsonify("ID Obrigatorio"), 400 # Retorna BAD REQUEST - 400