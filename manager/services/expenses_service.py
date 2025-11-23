from manager.models.expenses import Expense
from werkzeug.datastructures.structures import MultiDict
from werkzeug.datastructures.headers import Headers
from utils.safe_route import check_connection, require_cr
from utils.check_field import check_field
from utils.now import now, timedelta
from flask import jsonify
from utils.db import db

class ExpenseService:
    @require_cr
    @check_connection
    def get(self, bd:MultiDict, hd:Headers, cr = None): # Pega as despesas
        dia = bd.get("dia", False)
        mes = bd.get("mes", False)
        ano = bd.get("ano", False)
        
        expenses = Expense._search_by_date(dia, mes, ano, cr)
        return jsonify(expenses), 200

    @require_cr
    @check_connection
    def create(self, bd:MultiDict, hd:Headers, cr = None): # Cria uma despesa
        valor = bd.get("valor")
        motivo = bd.get("motivo")
        mat = bd.get("mat")
        
        ok, error = check_field(valor=valor, motivo=motivo, matricula=mat)
        
        if ok:
            expense = Expense()
            expense.valor = valor
            expense.data = now()
            expense.motivo = motivo
            expense.matricula = mat
            expense.cr = cr
            db.session.add(expense)
            db.session.commit()
            return jsonify({
                "msg": "Despesa adicionada com sucesso",
                "id": expense.id,
                "ok": True
            }), 200
        return jsonify(error), 400
        
    @require_cr
    @check_connection
    def update(self, bd:MultiDict, hd:Headers, cr = None): # atualiza os dados de um Despesa
        id = bd.get("id")
        valor = bd.get("valor")
        motivo = bd.get("motivo")
        mat = bd.get("mat")

        if id:
            expense = Expense.query.filter_by(id=id).one()
            if valor: expense.valor = valor
            if motivo: expense.motivo = motivo
            if mat: expense.mat = mat

            return jsonify("Dados atualizados com sucesso"), 200
        return jsonify("Id Obrigatório"), 401
            
    @require_cr
    @check_connection
    def delete(self, bd:MultiDict, hd:Headers, cr = None): # Exclui a despesa
        id = bd.get("id")
        if id:
            db.session.delete(Expense.query.get(id))
            db.session.commit()
            return jsonify("Excluso com sucesso"), 200
        return jsonify("ID Obrigatório"), 400

