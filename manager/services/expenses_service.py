from manager.models.expenses import Expense
from werkzeug.datastructures.structures import MultiDict
from werkzeug.datastructures.headers import Headers
from utils.safe_route import check_connection, require_cr
from utils.check_field import check_field
from utils.now import now
from flask import jsonify
from utils.db import db
from manager.models.timezone import fuso
from dateutil.relativedelta import relativedelta

class ExpenseService:
    # @check_connection
    @require_cr
    def get(self, bd:MultiDict, cr = None): # Pega as despesas
        id = bd.get("id")
        date = bd.get("data")
        if id: return jsonify(Expense.get_expense(id, cr)), 200 # Retorna por ID
        if date: # Retorna pela data informada no args (DD-MM-YYYY)
            formated_dt = now().strptime(date, "%d-%m-%Y") # Formata a data pro estilo UTC
            return jsonify(Expense._search_all_by_date(cr, formated_dt)) # Retorna as despesas pela data declarada caso haja alguma
        return jsonify(Expense._search_default(cr)), 200 # Retorna o default - a partir de 3 meses atras

    @check_connection
    @require_cr
    def create(self, bd:MultiDict, hd:Headers, cr = None): # Cria uma despesa
        value = bd.get("valor") # Valor da Despesa
        reason = bd.get("motivo") # Motivo da Despesa
        mat = bd.get("mat") # Matricula do Func.
        
        # Checka os campos - Evita ficar fazendo "IFS"
        ok, error = check_field(valor=value, motivo=reason, matricula=mat)
        
        # Caso passe na verificação da continuidade
        if ok:
            expense = Expense( # Cria a expense
                valor = value,
                data = now(fuso(cr)),
                motivo = reason.upper(),
                matricula = mat,
                cr = cr
            )
            db.session.add(expense) # Add a mesma a tabela
            db.session.commit() # Commita
            return jsonify({ # Retonrno
                "msg": "Despesa criada",
                "id": expense.id,
            }), 201 # Retorna create, o id e a mensagem
        return jsonify(error), 400 # Caso não passe na veridicação retorna BAD REQUEST - 400
        
    @check_connection
    @require_cr
    def update(self, bd:MultiDict, hd:Headers, cr = None): # atualiza os dados de um Despesa
        id = bd.get("id") # ID da  Despesa, sendo obrigatório claro
        value = bd.get("valor") # Valor a ser alterado
        reason = bd.get("motivo") # Motivo a ser alterado
        mat = bd.get("mat") # Matricula para alterar

        if id:
            expense = Expense.query.filter_by(id=id).first() # Busca a despesa
            if expense: # Caso encontre atualiza os valores
                if value: expense.valor = value
                if reason: expense.motivo = reason
                if mat: expense.mat = mat
                return jsonify("Despesa atualizada"), 200 # Retorna
            return jsonify("Despesa não encontrada"), 404
        return jsonify("Id Obrigatório"), 400
            
    @check_connection
    @require_cr
    def delete(self, bd:MultiDict, hd:Headers, cr = None): # Exclui a despesa
        id = bd.get("id")
        if id:
            db.session.delete(Expense.query.get(id))
            db.session.commit()
            return jsonify("Despesa removida com sucesso"), 200
        return jsonify("ID Obrigatório"), 400

