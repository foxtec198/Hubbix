# Utils
from utils.safe_route import safe_route
from flask import jsonify, request as rq
from utils.now import now
from utils.db import db, query
from manager.models.timezone import fuso
# Models
from manager.models.pos import Pos, PosClose, Items
from manager.models.employees import Employee
from manager.models.sales import Sale
from manager.models.expenses import Expense
from manager.models.products import Product
from manager.models.employees import Employee

class PosService:
    @safe_route
    def status(self, token_data): # Confere se o caixa está aberto, e retorna os dados do caixa
        cr = token_data.get("cr")
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
 
    @safe_route
    def open(self, token_data): # Abre o caixa se ná não estiver aberto
        body = rq.form
        cr = token_data.get("cr")
        mat = body.get("mat")
        valor = body.get("valor", 0)
        if not Pos.check(cr):
            if mat:
                emp = Employee._search_by_mat(mat, cr)
                if emp:
                    if emp.permissao == "ADMIN":
                        pos = Pos(
                            abertura = valor, matricula = mat,
                            data = now(fuso(cr)), cr = cr, valor = valor
                        )
                        db.session.add(pos)
                        db.session.commit()
                        return jsonify("Caixa aberto com sucesso!"), 200
                    return jsonify("Você não tem permissão!"), 401
                return jsonify("Funcionario não encontrado"), 404
            return jsonify("Matricula Obrigatória"), 400
        return jsonify("Caixa já aberto"), 406

    @safe_route
    def append(self, token_data): # Adiciona valor ao caixa
        cr = token_data.get("cr")
        body = rq.form
        mat = body.get("mat")
        if Pos.check(cr):
            emp = Employee._search_by_mat(mat, cr)
            if emp:
                if emp.permissao == "ADMIN":
                    valor = float(body.get("valor", 0))
                    cash = Pos.query.filter_by(cr=cr).one()
                    cash.valor += valor
                    db.session.commit()
                    return jsonify("Valor atualizado com sucesso"), 200
                return jsonify("Você não tem permissão!"), 401
            return jsonify("Matricula nao encontrada!"), 404
        return jsonify("Caixa fechado!"), 401

    @safe_route
    def close(self, token_data): # Fecha o caixa
        mat = rq.args.get("mat")
        cr = token_data.get("cr")
        gc = token_data.get("gc")
        
        if mat:
            emp = Employee._search_by_mat(mat, cr)
            if emp:
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
                
                # Dados do fechamento
                caixa_fc = PosClose()
                caixa_fc.abertura = dd["ABERTURA"]
                caixa_fc.cartao = dd["DEBITO"] + dd["CREDITO"]
                caixa_fc.dinheiro = dd["DINHEIRO"]
                caixa_fc.pix = dd["PIX"]
                caixa_fc.total = dd["TOTAL"]
                caixa_fc.saida = dd["DESPESAS"]
                caixa_fc.cr = cr
                caixa_fc.troco = dd["FECHAMENTO"]
                caixa_fc.grupodecliente = gc
                caixa_fc.matricula = mat
                caixa_fc.data = now(fuso(cr))

                db.session.add(caixa_fc)
                db.session.delete(caixa_atual)
                db.session.commit()
                return jsonify("Caixa fechado com sucesso"), 200 # Retorna sucesso
            return jsonify("Funcionario não encontrado"), 404 # Retorna NOT FOUND - 404
        return jsonify("Matrícula é obrigatória"), 400 # Retorna BAD REQUEST - 400

    @safe_route
    def last_close(self, token_data) -> tuple: # Retorna o valor do troco do último fechamento
        cr = token_data.get("cr")
        return jsonify(PosClose.check(cr).troco), 200 

    # ===============================================================
    # ===============================================================
    # ====================== MODO CAIXA =============================
    # ===============================================================
    # ===============================================================

    @safe_route
    def get_products(self, token_data):
        cr = token_data.get("cr")
        pos_itens = Items.query.filter_by(cr=cr).all()
        return jsonify([item.to_dict() for item in pos_itens])

    @safe_route
    def set_products(self, token_data):
        cr = token_data.get("cr")
        ean = rq.args.get("ean")
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
    
    @safe_route
    def clean_pos(self, token_data):
        cr = token_data.get("cr")
        query("delete from md_items_caixa where cr = '%s'", cr)
        return jsonify("Excluso com sucesso")

    