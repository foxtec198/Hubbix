from flask import Blueprint, request as rq
from manager.services.expenses_service import ExpenseService

expenses_bp = Blueprint("Despesas", __name__)
expense_service = ExpenseService()

@expenses_bp.route("", methods=["GET","POST","PATCH","DELETE"])
def main():
    match rq.method:
        case "GET": return expense_service.get() # Retorna os valores 
        case "POST": return expense_service.create() # Cria uma despesa
        case "PATCH": return expense_service.update() # Altera os dados da despesa
        case "DELETE": return expense_service.delete() # Remove a despesa
