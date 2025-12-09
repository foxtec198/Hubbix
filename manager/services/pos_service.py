from werkzeug.datastructures.headers import Headers
from werkzeug.datastructures.structures import MultiDict
from utils.safe_route import require_cr, check_connection
from flask import jsonify
from utils.now import now

from manager.models.pos import Pos, PosClose, Items
from manager.models.employess import Employee
from manager.models.sales import Sale
from manager.models.expenses import Expense
from manager.models.timezone import fuso
from utils.db import db, query
from manager.models.products import Product

class PosService:
    @check_connection
    @require_cr
    def status(self, bd:MultiDict, hd:Headers, cr=None): # Confere se o caixa está aberto, e retorna os dados do caixa
        cash = Pos.query.filter_by(cr=cr).first()
        if cash: return jsonify({
            "status": True,
            "valor": cash.valor,
            "abertura": cash.abertura,
            "data": cash.data,
            "matricula": cash.matricula,
        })
        return jsonify({
            "status": False,
            "msg": "Caixa fechado",
            "hint": "Abra o caixa pela URI /caixa com método POST",
        })

    @check_connection 
    @require_cr
    def open(self, bd:MultiDict, hd:Headers, cr=None): # Abre o caixa se ná não estiver aberto
        if not Pos.query.filter_by(cr=cr).first():
            mat = bd.get("mat")
            emp = Employee._search_by_mat(mat, cr)
            if emp.permissao == "ADMIN":
                valor = bd.get("valor", 0)
                if valor > 0:
                    cash = Pos()
                    cash.valor = valor            
                    cash.abertura = valor            
                    cash.matricula = mat
                    cash.data = now(fuso(cr))
                    cash.cr = cr
                    db.session.add(cash)
                    db.session.commit()
                    return jsonify("Caixa aberto com sucesso!"), 200
                return jsonify("Valor precisa ser maior que zero!"), 400
            return jsonify("Você não tem permissão!"), 401
        return jsonify("Caixa já aberto"), 401

    @check_connection
    @require_cr
    def append(self, bd:MultiDict, hd:Headers, cr=None): # Adiciona valor ao caixa
        mat = bd.get("mat")
        emp = Employee._search_by_mat(mat, cr)
        if emp.permissao == "ADMIN":
            valor = bd.get("valor", 0)
            if valor > 0:
                cash = Pos.query.filter_by(cr=cr).one()
                cash.valor += valor
                db.session.commit()
                return jsonify("Valor atualizado com sucesso"), 200
            return jsonify("Valor precisa ser maior que zero"), 400
        return jsonify("Você não tem permissão!"), 401

    @check_connection
    @require_cr
    def close(self, bd:MultiDict, hd:Headers, cr=None): # Fecha o caixa
        mat = bd.get("mat")
        gc = hd.get("gc")
        
        if mat:
            vendas = Sale.query.filter_by(cr=cr, data=now(fuso(cr)).today()).all()
            
            dd = {'PIX':0, 'DINHEIRO':0, 'DEBITO':0, 'CREDITO':0, 'TOTAL': 0, 'DESPESAS':0, 'ABERTURA':0, "FECHAMENTO":0}

            for venda in vendas:
                dd[venda.pagamento] += venda.valor - venda.desconto
                dd["TOTAL"] += venda.valor - venda.desconto
            
            saidas = Expense.query.filter_by(cr=cr, data=now(fuso(cr)).today()).all()
            
            for saida in saidas: dd["DESPESAS"] += saida.valor

            caixa_atual = Pos.query.filter_by(cr=cr).one()
            dd["ABERTURA"] = caixa_atual.abertura
            dd["FECHAMENTO"] = caixa_atual.valor
            
            print(dd)

            # Dados do fechamento
            caixa_fc = PosClose()
            caixa_fc.abertura = dd["ABERTURA"]
            caixa_fc.cartao = dd["DEBITO"] + dd["CREDITO"]
            caixa_fc.dinheiro = dd["DINHEIRO"]
            caixa_fc.pix = dd["PIX"]
            caixa_fc.total = dd["TOTAL"]
            caixa_fc.saida = dd["DESPESAS"]
            caixa_fc.cr = cr
            caixa_fc.grupodecliente = gc
            caixa_fc.matricula = mat
            caixa_fc.data = now(fuso(cr))

            db.session.add(caixa_fc)
            db.session.delete(caixa_atual)
            db.session.commit()
            return jsonify("Caixa fechado com sucesso"), 200
        return jsonify("Matrícula é obrigatória"), 400
            
    # ===============================================================
    # ===============================================================
    # ====================== MODO CAIXA =============================
    # ===============================================================
    # ===============================================================

    @check_connection
    @require_cr
    def get_products(self, bd:MultiDict, hd:Headers, cr=None):
        pos_itens = Items.query.filter_by(cr=cr).all()
        return jsonify([item.to_dict() for item in pos_itens])

    @check_connection
    @require_cr
    def set_products(self, ean, cr=None):
        if ean:
            prod = Product._search_by_ean(ean)
            items = Items.query.filter_by(ean=ean).first()
            # Confirma se já tem um prod adicionado e adiciona a quantidade
            if items: 
                items.quantidade += 1
                items.total = items.quantidade * items.valor
            else: # Se nao tiver cria um
                items = Items()
                items.id_item = prod.id
                items.ean = prod.ean
                items.nome = prod.nome
                items.quantidade = 1
                items.valor = prod.valor
                items.total = prod.valor
                items.cr = cr
                db.session.add(items)
            db.session.commit()
            return jsonify("Sucesso"), 200
        return jsonify("EAN Obrigatório"), 400
    
    @check_connection
    @require_cr
    def clean_pos(self, cr=None):
        query("delete from md_items_caixa where cr = '%s'", cr)
        return jsonify("Excluso com sucesso")

    