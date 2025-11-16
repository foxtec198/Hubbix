from flask import Blueprint, jsonify, request as rq
from manager.services.employees_service import EmployeeService

employees_bp = Blueprint("Funcionarios", __name__)
employee_service = EmployeeService()

@employees_bp.route("/", methods=['GET', 'POST', 'PATCH', 'DELETE'])
def main():
    match rq.method:
        case "GET": # Retorna todos os dados de Funcionarios
            return employee_service.get(rq.headers)
            
        case "POST": # Criar um novo Funcionario
            return employee_service.create(rq.get_json(), rq.headers)
            
        case "PATCH": # Atualiza os dados de Funcionarios existentes
            return employee_service.update(rq.get_json(), rq.headers)
            
        case "DELETE": # Remove funcionarios
            return employee_service.delete(rq.args, rq.headers)
            
    return jsonify("Erro interno"), 500