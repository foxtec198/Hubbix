from flask import jsonify
from werkzeug.datastructures import MultiDict, Headers
from utils.safe_route import check_connection, require_cr
from utils.check_field import check_field
from manager.models.mercado_pago import MP
from manager.models.sales import Sale
from utils.db import db

class MPService:
    mp = MP()

    @check_connection
    @require_cr
    def get_payment_status(self, bd:MultiDict, hd:Headers, cr=None): # Pega o status do pagamento
        # Dados Obrigatorio
        id = bd.get('id')
        key = bd.get('key')

        # Checa os campos obrigatorios
        ok, error = check_field(id=id,key=key)
        
        if ok: # se ok da continuidade
            res = self.mp.get_merchant_order(key) # Pega o id da venda no MP
            status = res.get('elements')[0].get('status') # Pega o status do pagamento
            # Confirma o status do pagamento
            if status == 'closed': 
                Sale.query.fikter_by(id=id).one().pix_pago = True
                db.session.commit()
                return jsonify('Sucesso'), 200
            return jsonify({'status': status, 'msg': 'Aguardando pagamento.'}), 402
        return jsonify(error), 400