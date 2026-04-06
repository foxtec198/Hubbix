# Utils
from flask import jsonify, request as rq
from utils.safe_route import safe_route
from utils.check_field import check_field
# Models
from manager.models.sales import Sale, db
from manager.models.mercado_pago import MP

class MPService:
    mp = MP()

    @safe_route
    def get_payment_status(self, token_data): # Pega o status do pagamento
        # Dados Obrigatorio
        body = rq.get_json()
        
        id = body.get('id')
        key = body.get('key')

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