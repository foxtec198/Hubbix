from flask import Blueprint, request as rq, jsonify
from manager.services.expenses_service import ExpenseService

expenses_bp = Blueprint("Despesas", __name__)
expense_service = ExpenseService()

@expenses_bp.route("/", methods=["GET","POST","PATCH","DELETE"])
def main():
    match rq.method:
        case "GET": return expense_service.get(rq.args) # Retorna os valores 
        case "POST": return expense_service.create(rq.get_json(), rq.headers) # Cria uma despesa
        case "PATCH": return expense_service.update(rq.get_json(), rq.headers) # Altera os dados da despesa
        case "DELETE": return expense_service.delete(rq.args, rq.headers) # Remove a despesa
    return jsonify("Metodo não permitido"), 405