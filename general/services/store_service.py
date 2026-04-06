from werkzeug.datastructures import MultiDict, Headers
from utils.safe_route import check_connection, safe_route
from general.models.store import Store
from manager.models.config import Config
# frmo gourmet.models.config import Config as GConfig
from flask import jsonify
from utils.db import db

class StoreService:
    @check_connection
    @safe_route
    def get_store_data(self, cr=None): # Retorna os dados da Loja
        store = Store.query.filter_by(cr=cr).first()
        if store: 
            # config = Config.query.filter_by(cr=cr).first() | GConfig.query.filter_by(cr=cr).first()
            config = Config.query.filter_by(cr=cr).first()
            if config:
                return jsonify({
                    "loja": store.to_dict(),
                    "logo": config.logo
                })
            return jsonify("Configuração nao encontrada"), 404
        return jsonify("Loja nao encontrada"), 404

    @check_connection
    @safe_route
    def create_store(self, bd:MultiDict, hd:Headers, cr=None):
        ...

    @check_connection
    @safe_route
    def update_store(self, bd:MultiDict, hd:Headers, cr=None):
        nome = bd.get("nome")
        bairro = bd.get("bairro")
        cep = bd.get("cep")
        cidade = bd.get("cidade")
        estado = bd.get("estado")
        rua = bd.get("rua")
        negociante = bd.get("negociante")
        pacote = bd.get("pacote")
        sistema = bd.get("sistema")
        situacao = bd.get("situacao")
        telefone = bd.get("telefone")
        email = bd.get("email")
        external_pos_id = bd.get("external_pos_id")
        user_id = bd.get("user_id")
        idLoja = bd.get("idLoja")

        store = Store.query.filter_by(cr=cr).first()

        if store:
            if nome: store.nome_loja = nome.upper()
            if bairro: store.bairro = bairro.upper()
            if cep: store.cep = cep
            if cidade: store.cidade = cidade.upper()
            if estado: # Confirma se o estado esta em UF
                if len(estado) == 2: store.estado = estado.upper()
                else: return jsonify("Estado deve estar no estile UF, Exemplo: PR, MS, MG, SC"), 400 
            if rua: store.rua = rua.upper()
            if negociante: store.negociante = negociante.upper()
            if pacote: store.pacote = pacote.upper()
            if sistema: store.sistema = sistema.lower()
            if situacao: store.situacao = situacao.capitalize()
            if telefone: store.telefone = telefone
            if email: store.email = email
            if external_pos_id: store.external_pos_id = external_pos_id
            if user_id: store.user_id = user_id
            if idLoja: store.idLoja = idLoja
            db.session.commit()
            return jsonify("Dados alterados com sucesso"), 200
        return jsonify("Loja nao encontrada"), 404

    @check_connection
    @safe_route
    def delete_store(self, bd:MultiDict, hd:Headers, cr=None):
        ...
