from flask import Blueprint, jsonify, request as rq
from manager.services.employees_service import EmployeeService

employees_bp = Blueprint("Funcionarios", __name__)
employee_service = EmployeeService()

@employees_bp.route("", methods=['GET', 'POST', 'PATCH', 'DELETE'])
def main():
    match rq.method:
        case "GET": return employee_service.get(rq.args) # Retorna todos os dados de Funcionarios
        case "POST":  return employee_service.create(rq.get_json(), rq.headers) # Criar um novo Funcionario
        case "PATCH": return employee_service.update(rq.get_json()) # Atualiza os dados de Funcionarios existentes
        case "DELETE": return employee_service.delete(rq.args) # Remove funcionarios
