# Utils
from utils.safe_route import safe_route
from utils.check_field import check_field
from flask import jsonify, request as rq
from utils.now import now
from utils.db import db
from manager.models.timezone import fuso
# Models
from manager.models.expenses import Expense
from manager.models.pos import Pos

class ExpenseService:
    @safe_route
    def get(self, token_data):
        """
        Docstring for get expenses
        
        :return: (JSON, CODE)
        :rtype: tuple[Response, Literal[200]]
        """

        args = rq.args
        cr = token_data.get("cr")
        id = args.get("id") # ID da Despesa
        date = args.get("data") # Data
        # Caso seja passado o id retorna a Despesa exclusiva
        if id: return jsonify(Expense.get_expense(id, cr)), 200 # Retorna sucesso
        if date: # Retorna pela data informada no args (DD-MM-YYYY)
            formated_dt = now().strptime(date, "%d-%m-%Y") # Formata a data pro estilo UTC
            return jsonify(Expense._search_all_by_date(cr, formated_dt)), 200 # Retorna as despesas pela data declarada caso haja alguma
        return jsonify(Expense._search_default(cr)), 200 # Retorna o default - a partir de 3 meses atras

    @safe_route
    def create(self, token_data):
        """
        Docstring for create
        
        :return: (JSON, CODE)
        :rtype: tuple[Response, Literal[201]] | tuple[Response, Literal[400]]
        """

        cr = token_data.get("cr")
        body = rq.get_json()
        value = float(body.get("valor")) # Valor da Despesa
        reason = body.get("motivo") # Motivo da Despesa
        mat = body.get("mat") # Matricula do Func.
        
        # Checka os campos - Evita ficar fazendo "IFS"
        ok, error = check_field(valor=value, motivo=reason, matricula=mat)
        
        # Caso passe na verificação da continuidade
        if ok:
            expense = Expense( # Cria a expense
                valor = value, data = now(fuso(cr)),
                motivo = reason.upper(), matricula = mat, cr = cr
            )
            Pos.add_expense_to_Pos(cr, value)
            db.session.add(expense) # Add a despesa na tabela
            db.session.commit() # Salva os registros
            return jsonify({ "msg": "Despesa criada", "expense": expense.to_dict() }), 201 # Retorna create, o id e a mensagem
        return jsonify(error), 400 # Caso não passe na veridicação retorna BAD REQUEST - 400
    
    @safe_route
    def update(self, token_data):
        """
        Docstring for update
        
        :return: (JSON, CODE)
        :rtype: tuple[Response, Literal[200]] | tuple[Response, Literal[404]] | tuple[Response, Literal[400]]
        """

        body = rq.get_json()
        cr = token_data.get("cr")
        id = body.get("id") # ID da Despesa
        value = body.get("valor") # Valor a ser alterado
        reason = body.get("motivo") # Motivo a ser alterado
        mat = body.get("mat") # Matricula para alterar

        if id: # Confere se foi declarado o ID
            expense = Expense._search_by_id(cr, id) # Busca a despesa
            if expense: # Caso encontre atualiza os valores
                if value: expense.valor = value # Atualiza o valor se declarado
                if reason: expense.motivo = reason # Atualiza o motivo se declarado
                if mat: expense.mat = mat # Atualiza a matricula se declarada
                return jsonify("Despesa atualizada"), 200 # Retorna Sucesso
            return jsonify("Despesa não encontrada"), 404 # Retorna NOT FOUND - 404
        return jsonify("Id Obrigatório"), 400 # Retorna BAD REQUEST - 400
            
    @safe_route
    def delete(self):
        """
        Docstring for update
        
        :return: (JSON, CODE)
        :rtype: tuple[Response, Literal[200]] | tuple[Response, Literal[400]]
        """

        id = rq.args.get("id") # Id da despesa
        if id: # Confere se foi declarado o Id
            db.session.delete(Expense.query.get(id)) # Remove da tabela
            db.session.commit() # Salva os dados
            return jsonify("Despesa removida"), 200 # Retorna sucesso
        return jsonify("Id Obrigatório"), 400 # Retorna BAD REQUEST - 400

