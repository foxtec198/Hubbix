# Utils
from utils.safe_route import safe_route
from manager.models.timezone import fuso
from flask import jsonify, request as rq
from utils.check_field import check_field
from utils.db import db
from utils.now import now
# Models
from manager.models.sales import Sale

class SalesService:
    @safe_route
    def get(self, token_data): # Obtem todas as vendas por ID ou CR
        args = rq.args
        cr = token_data.get("cr")
        id = args.get("id")
        month = args.get("month")
        day = args.get("day")
        year= args.get("year")
        if id: 
            sale = Sale._search_by_id(id).first()
            if sale: return jsonify(sale.to_dict())
            return jsonify("Funcionario nao encontrado"), 404
        if day and month and year: return jsonify(Sale._search_by_date(day, month, year, cr))
        else: return jsonify(Sale._search_by_cr(cr))

    @safe_route
    def create(self, token_data): # Cria uma nova venda
        bd = rq.get_json()
        cr = token_data.get("cr")
        gc = token_data.get("gc")

        valor = bd.get("valor") # Valor da Venda
        desconto = bd.get("desconto") # Valor do desconto
        pagamento = bd.get("pagamento") # Metodo de pagamento
        id_cliente = bd.get("id_cliente", 0) # Obtem o id do cliente, caso contrario define como 0(Não informado)
        tipo = bd.get("tipo", "PRODUTOS") # Tipo Produtos/OS
        matricula = bd.get("mat") # Matricula
        data = now(fuso(cr)) # Data atual

        ok, error = check_field( # Confirma os valres obrigatorios.
            valor=valor,
            pagamento=pagamento,
            id_cliente=id_cliente,
            tipo=tipo,
            matricula=matricula
        )
        
        if ok: # Confere se os dados estão ok
            nova_venda = Sale(
                valor=valor, cr=cr, pagamento=pagamento, 
                desconto=desconto, data=data, grupodecliente=gc
            ) # Cria a nvoa venda
            db.session.add(nova_venda) # Adiciona a nova venda na sessao
            db.session.commit() # Salva a nova venda no bd 
            return jsonify(nova_venda.to_dict()), 201 # Retorna create com a nova venda e seus dados!
        return jsonify(error), 400 # Retorna um bad request com o campo faltante
