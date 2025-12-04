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
        valor = bd.get("valor")
        desconto = bd.get("desconto")
        pagamento = bd.get("pagamento")
        id_cliente = bd.get("id_cliente", 0) # Obtem o id do cliente, caso contrario define como 0(Não informado)
        data = now(fuso(cr))
        grupodecliente = hd.get("grupodecliente")
        cr = cr
        tipo = bd.get("tipo", "PRODUTOS")
        matricula = bd.get("mat")

        ok, error = check_field(
            valor=valor,
            pagamento=pagamento,
            id_cliente=id_cliente,
            tipo=tipo,
            matricula=matricula
        )
        
        nova_venda = Sale(
        )

        db.session.add(nova_venda)
        db.session.commit()
        return jsonify(nova_venda.to_dict()), 201
