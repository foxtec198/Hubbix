from flask import Blueprint, request as rq
from manager.services.employees_service import EmployeeService

employees_bp = Blueprint("Funcionarios", __name__)
employee_service = EmployeeService()

@employees_bp.route("", methods=['GET', 'POST', 'PATCH', 'DELETE'])
def main():
    match rq.method:
        case "GET": return employee_service.get() # Retorna todos os dados de Funcionarios
        case "POST":  return employee_service.create() # Criar um novo Funcionario
        case "PATCH": return employee_service.update() # Atualiza os dados de Funcionarios existentes
        case "DELETE": return employee_service.delete() # Remove funcionarios
