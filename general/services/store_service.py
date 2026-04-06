from utils.safe_route import safe_route
from general.models.store import Store
from manager.models.config import Config
from flask import jsonify, request as rq
from utils.db import db

class StoreService:
    @safe_route
    def get_store_data(self, token_data): # Retorna os dados da Loja
        cr = token_data.get("cr")
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

    @safe_route
    def create_store(self, token_data):
        cr = token_data.get("cr")
        return 
    
    @safe_route
    def update_store(self, token_data):
        cr = token_data.get("cr")
        body = rq.get_json()

        nome = body.get("nome")
        bairro = body.get("bairro")
        cep = body.get("cep")
        cidade = body.get("cidade")
        estado = body.get("estado")
        rua = body.get("rua")
        negociante = body.get("negociante")
        pacote = body.get("pacote")
        sistema = body.get("sistema")
        situacao = body.get("situacao")
        telefone = body.get("telefone")
        email = body.get("email")
        external_pos_id = body.get("external_pos_id")
        user_id = body.get("user_id")
        idLoja = body.get("idLoja")

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

    @safe_route
    def delete_store(self, token_data):
        cr = token_data.get("cr")
        return
