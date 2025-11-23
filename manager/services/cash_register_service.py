from werkzeug.datastructures.headers import Headers
from werkzeug.datastructures.structures import MultiDict
from utils.safe_route import require_cr, check_connection
from flask import jsonify
from sqlalchemy import Date, cast
from utils.now import now

from manager.models.cash_register import CashRegister, CashRegisterClose
from manager.models.employess import Employee
from manager.models.sales import Sale
from manager.models.expenses import Expense
from utils.db import db

class CashRegisterService:
    @require_cr
    @check_connection
    def status(self, bd:MultiDict, hd:Headers, cr=None): # Confere se o caixa está aberto, e retorna os dados do caixa
        cash = CashRegister.query.filter_by(cr=cr).one()
        if cash: return jsonify({
            "status": True,
            "valor": cash.valor,
            "abertura": cash.abertura,
            "data": cash.data,
            "matricula": cash.matricula,
        })
        return jsonify({"status": False})

    @require_cr
    @check_connection 
    def open(self, bd:MultiDict, hd:Headers, cr=None): # Abre o caixa se ná não estiver aberto
        if not CashRegister.query.filter_by(cr=cr).one():
            mat = bd.get("mat")
            emp = Employee._search_by_mat(mat, cr)
            if emp.permissao == "ADMIN":
                valor = bd.get("valor", 0)
                if valor > 0:
                    cash = CashRegister()
                    cash.valor = valor            
                    cash.abertura = valor            
                    cash.matricula = mat
                    cash.data = now()
                    cash.cr = cr
                    db.session.add(cash)
                    db.session.commit()
                    return jsonify("Caixa aberto com sucesso!"), 200
                return jsonify("Valor precisa ser maior que zero!"), 400
            return jsonify("Você não tem permissão!"), 401
        return jsonify("Caixa já aberto"), 401

    @require_cr
    @check_connection
    def append(self, bd:MultiDict, hd:Headers, cr=None): # Adiciona valor ao caixa
        mat = bd.get("mat")
        emp = Employee._search_by_mat(mat, cr)
        if emp.permissao == "ADMIN":
            valor = bd.get("valor", 0)
            if valor > 0:
                cash = CashRegister.query.filter_by(cr=cr).one()
                cash.valor += valor
                db.session.commit()
                return jsonify("Valor atualizado com sucesso"), 200
            return jsonify("Valor precisa ser maior que zero"), 400
        return jsonify("Você não tem permissão!"), 401

    @require_cr
    @check_connection
    def close(self, bd:MultiDict, hd:Headers, cr=None): # Fecha o caixa
        gc = hd.get("gc")
        vendas = Sale.query.filter_by(cr=cr, data=now().today()).all()
        
        dd = {'PIX':0, 'DINHEIRO':0, 'DEBITO':0, 'CREDITO':0, 'TOTAL': 0, 'DESPESAS':0, 'ABERTURA':0, "FECHAMENTO":0}

        for venda in vendas:
            dd[venda.pagamento] += venda.valor - venda.desconto
            dd["TOTAL"] += venda.valor - venda.desconto
        
        saidas = Expense.query.filter_by(cr=cr, data=now().today()).all()
        
        for saida in saidas: dd["DESPESAS"] += saida.valor

        caixa_atual = CashRegister.query.filter_by(cr=cr).one()
        dd["ABERTURA"] = caixa_atual.abertura
        dd["FECHAMENTO"] = caixa_atual.valor
        
        caixa_fc = CashRegisterClose()
        caixa_fc.abertura = dd["ABERTURA"]
        caixa_fc.cartao = dd["DEBITO"] + dd["CREDITO"]
        caixa_fc.dinheiro = dd["DINHEIRO"]
        caixa_fc.pix = dd["PIX"]
        caixa_fc.total = dd["TOTAL"]
        caixa_fc.saida = dd["DESPESAS"]
        caixa_fc.cr = cr
        caixa_fc.grupodecliente = gc
        # Falta matricula, data
        
        db.session.add(caixa_fc)
        db.session.commit()
        return jsonify("Caixa fechado com sucesso"), 200
            
        