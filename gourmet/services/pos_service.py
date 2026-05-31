from flask import jsonify, request as rq
from utils.safe_route import safe_route
from utils.now import now
from gourmet.models.pos import POSOpen, POSClosed, POSApplied
from gourmet.models.sales import Sale
from gourmet.models.config import Config
from utils.db import db

class POSService:
    @safe_route
    def status(self, token_data):
        cr = token_data.get('cr')
        pos = POSOpen._search_by_cr(cr)
        return jsonify(pos.to_dict() if pos else False), 200

    @safe_route
    def open(self, token_data):
        data = rq.get_json()
        cr = token_data.get('cr')
        perm = token_data.get('perm')
        valor = data.get('valor')

        if not valor:
            return jsonify({'error': 'Valor obrigatório'}), 400

        if perm != 'ADMIN':
            return jsonify({'error': 'Você não tem permissão'}), 401

        if POSOpen._search_by_cr(cr):
            return jsonify({'error': 'Caixa já está aberto'}), 401

        pos = POSOpen(cr=cr, valor=valor, caixa_abertura=valor)
        db.session.add(pos)
        db.session.commit()
        return jsonify({'msg': 'Caixa aberto com sucesso'}), 200

    @safe_route
    def check(self, token_data):
        cr = token_data.get('cr')
        pos = POSOpen._search_by_cr(cr)

        if not pos:
            return jsonify(False), 200

        result = {
            'debito': 0,
            'credito': 0,
            'pix': 0,
            'dinheiro': 0,
            'total': 0,
            'abertura': pos.caixa_abertura,
            'fechamento': pos.valor,
        }

        sales = db.session.query(Sale).filter(
            Sale.cr == cr,
            Sale.data >= pos.data
        ).all()

        for sale in sales:
            result['debito'] += sale.debito
            result['credito'] += sale.credito
            result['pix'] += sale.pix
            result['dinheiro'] += sale.dinheiro
            result['total'] += (sale.debito + sale.credito + sale.pix + sale.dinheiro)

        return jsonify(result), 200

    @safe_route
    def apply(self, token_data):
        data = rq.get_json()
        cr = token_data.get('cr')
        perm = token_data.get('perm')
        mat = token_data.get('mat')
        valor = data.get('valor')

        if not valor or valor <= 0:
            return jsonify({'error': 'Valor deve ser maior que zero'}), 400

        if perm != 'ADMIN':
            return jsonify({'error': 'Operação não permitida'}), 401

        pos = POSOpen._search_by_cr(cr)
        if not pos:
            return jsonify({'error': 'Caixa fechado'}), 401

        applied = POSApplied(
            valor=valor,
            valor_abertura=pos.caixa_abertura,
            matricula=mat
        )
        db.session.add(applied)

        pos.valor += valor
        db.session.commit()
        return jsonify({'msg': 'Sucesso'}), 200

    @safe_route
    def close(self, token_data):
        cr = token_data.get('cr')
        perm = token_data.get('perm')
        mat = token_data.get('mat')
        gc = token_data.get('gc')

        if perm != 'ADMIN':
            return jsonify({'error': 'Operação não permitida'}), 401

        pos = POSOpen._search_by_cr(cr)
        if not pos:
            return jsonify({'error': 'Caixa já está fechado'}), 401

        closed = POSClosed(
            abertura=pos.caixa_abertura,
            fechamento=pos.valor,
            grupodecliente=gc,
            cr=cr,
            matricula=mat
        )
        db.session.add(closed)
        db.session.delete(pos)
        db.session.commit()

        return jsonify({'msg': 'Caixa fechado com sucesso'}), 200

    @safe_route
    def last_value(self, token_data):
        cr = token_data.get('cr')
        pos_closed = POSClosed._search_by_cr(cr)

        if pos_closed:
            return jsonify({'valor': pos_closed.fechamento}), 200
        return jsonify({'valor': None}), 200
