# Utils
from utils.safe_route import safe_route
from utils.now import now
from utils.db import db
from flask import jsonify, request as rq
from manager.models.timezone import fuso
# Models
from manager.models.releases import Release
from manager.models.sales import Sale
from manager.models.orders import Order
from manager.models.pos import Pos

class ReleaseService:
    @safe_route
    def get_releases(self, token_data): # Logica para obter as saidas
        # Retorna uma lista de saidas ou uma saida especifica se o id for declarado
        id = rq.args.get("id")
        cr = token_data.get("cr")
        if id: return Release.query.filter_by(id=id, cr=cr).one().to_dict()
        else: return [release.to_dict() for release in Release.query.filter_by(cr=cr).all()]

    @safe_route
    def create_release(self, token_data): # Logica para criar um saida
        ...

    @safe_route
    def update_release(self, token_data): # Logica para atualizar uma saida
        ...

    @safe_route
    def delete_release(self, token_data): # Logica para excluir uma saida
        bd = rq.args
        cr = token_data.get("cr")

        # Credenciais
        id_venda = bd.get('id_venda')
        id = bd.get('id')
        
        if id_venda:
            if id:
                if Pos.check(cr):
                    # Obtem a saida 
                    release = Release.query.filter_by(id=id, cr=cr).one()
                    value = release.valor

                    # Obtem a venda relacionada
                    sale = Sale.query.filter_by(id=id_venda, cr=cr).one()
                    payment = sale.pagamento
                    sale_value = sale.valor - sale.desconto
                    tipo = sale.tipo

                    # Se for OS cancela a Ordem
                    if tipo == 'OS': 
                        id_os = release.nome.strip('OS - NUM:')
                        Order.query.filter_by(id=id_os, cr=cr).one().situacao = "CANCELADA"
                        db.session.commit()

                    # Se for em dinheiro e caso tenha sido lançada no mesmo dia, retira do caixa
                    if payment == 'DINHEIRO' and sale.data.date() == now(fuso(cr)).date(): Pos.query.filter_by(cr=cr).one().valor -= sale_value

                    # Atualiza o valor da venda ou deleta se for 0
                    total = sale_value - value
                    if total == 0: db.session.delete(sale)
                    else: sale.valor = total
                    db.session.delete(release)
                    db.session.commit()
                    return jsonify('Sucesso'), 200
                return jsonify('Caixa fechado'), 400
            return jsonify('Id obrigatorio'), 400
        return jsonify('Id da Venda obrigatorio'), 400
    