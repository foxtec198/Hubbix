from werkzeug.datastructures.structures import MultiDict
from werkzeug.datastructures.headers import Headers                    
from utils.safe_route import require_cr, check_connection
from manager.models.sales import Sale
from manager.models.timezone import fuso
from flask import jsonify
from utils.check_field import check_field
from utils.db import db
from utils.now import now

class SalesService:
    @check_connection
    @require_cr
    def get(self, bd:MultiDict, cr=None): # Obtem todas as vendas por ID ou CR
        id = bd.get("id")
        month = bd.get("month")
        day = bd.get("day")
        year= bd.get("year")
        if id: return jsonify(Sale.query.filter_by(cr=cr, id=id).one().to_dict())
        if day and month and year: return jsonify(Sale._search_by_date(day, month, year, cr))
        else: return jsonify(Sale._search_by_cr(cr))

    def create(self, bd:MultiDict, hd:Headers, cr=None): # Cria uma nova venda
        valor = bd.get("valor") # Valor da Venda
        desconto = bd.get("desconto") # Valor do desconto
        pagamento = bd.get("pagamento") # Metodo de pagamento
        id_cliente = bd.get("id_cliente", 0) # Obtem o id do cliente, caso contrario define como 0(Não informado)
        data = now(fuso(cr)) # Data atual com fuso por loja
        grupodecliente = hd.get("gc") # Grupo de cliente 
        tipo = bd.get("tipo", "PRODUTOS") # Tipo Produtos/OS
        matricula = bd.get("mat") # Matricula

        ok, error = check_field( # Confirma os valres obrigatorios.
            valor=valor,
            pagamento=pagamento,
            id_cliente=id_cliente,
            tipo=tipo,
            matricula=matricula
        )
        if ok: # Confere se os dados estão ok
            nova_venda = Sale(valor=valor, cr=cr, pagamento=pagamento, desconto=desconto) # Cria a nvoa venda
            db.session.add(nova_venda) # Adiciona a nova venda na sessao
            db.session.commit() # Salva a nova venda no bd 
            return jsonify(nova_venda.to_dict()), 201 # Retorna create com a nova venda e seus dados!
        return jsonify(error), 400 # Retorna um bad request com o campo faltante
