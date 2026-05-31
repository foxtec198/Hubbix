# Utils
from utils.safe_route import safe_route
from manager.models.timezone import fuso
from flask import jsonify, request as rq
from utils.check_field import check_field
from utils.db import db
from utils.now import now
# Models
from manager.models.sales import Sale
from manager.models.products import Product
from manager.models.orders import Order
from manager.models.releases import Release, ViewRelease

class SalesService:
    @safe_route
    def get(self, token_data): # Obtem todas as vendas por ID ou CR
        filter = rq.args
        cr = token_data.get("cr")
        
        for value in filter:
            match value:
                case "id": 
                    return jsonify(Sale()._search_by_id(id).to_dict())

                case "month": 
                    return jsonify(ViewRelease._search_by_month(int(filter.get("month")), cr))

        return jsonify(Sale._search_by_cr(cr))

    @safe_route
    def create(self, token_data): # Cria uma nova venda
        bd = rq.get_json()
        cr = token_data.get("cr")
        gc = token_data.get("gc")

        valor = bd.get("valor") # Valor da Venda
        pagamento = bd.get("pagamento") # Metodo de pagamento
        matricula = int(bd.get("mat")) # Matricula
        desconto = bd.get("desconto", 0) # Valor do desconto
        id_cliente = bd.get("client_id", 0) # Obtem o id do cliente, caso contrario define como 0(Não informado)
        tipo = bd.get("tipo", "PRODUTOS") # Tipo Produtos/OS
        cart = bd.get("cart")
        data = now(fuso(cr)) # Data atual

        # Confirma os valres obrigatorios.
        ok, error = check_field(valor=valor, pagamento=pagamento, matricula=matricula)
        
        if ok: # Confere se os dados estão ok
            nova_venda = Sale(
                valor=valor, cr=cr, pagamento=pagamento, id_cliente=id_cliente, tipo=tipo,
                desconto=desconto, data=data, grupodecliente=gc, matricula=matricula
            ) # Cria a nvoa venda
            db.session.add(nova_venda) # Adiciona a nova venda na sessao

            for id in cart:
                quant = cart[id]
                match tipo:
                    case "PRODUTOS":
                        for i in range(quant):
                            produto = Product()._search_by_id(int(id))
                            db.session.add(Release(id_venda=nova_venda.id, nome=produto.nome, valor=produto.valor, custo=produto.custo, data=data, cr=cr, grupodecliente=gc))
                    case "OS":
                        os = Order()._search_by_id(int(id))
                        db.session.add(Release(id_venda=nova_venda.id, nome=f"OS - NUM: {id}", valor=os.valor, custo=os.custo, data=data, cr=cr, grupodecliente=gc))

            db.session.commit() # Salva a nova venda no bd 
            return jsonify(nova_venda.to_dict()), 201 # Retorna create com a nova venda e seus dados!
        return jsonify("Dados Obrigatórios: " + error), 400 # Retorna um bad request com o campo faltante
