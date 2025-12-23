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
    def get(self, bd:MultiDict, hd:Headers, cr=None): # Obtem todas as vendas por ID ou CR
        id = bd.get("id", None)
        if id: return jsonify(Sale.query.filter_by(cr=cr, id=id).one().to_dict())
        else: return jsonify([s.to_dict() for s in Sale.query.filter_by(cr=cr).all()])

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
        
        nova_venda = Sale( # Cria a nvoa venda
            valor=valor,
            cr=cr,
            pagamento=pagamento,
            desconto=desconto,
        )
        db.session.add(nova_venda)
        db.session.commit()
        return jsonify(nova_venda.to_dict()), 201
