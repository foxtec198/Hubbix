from hashlib import sha256
from flask import jsonify
from manager.models.employess import Employee, db
from werkzeug.datastructures.headers import Headers
from werkzeug.datastructures.structures import MultiDict
from utils.check_cr import check_cr

from utils.safe_route import require_cr, check_connection

class EmployeeService:
    @check_connection
    @require_cr
    def get(self, bd:MultiDict, hd:Headers, cr = None):
        return jsonify(Employee._search_by_cr(cr)), 200
        
    @check_connection
    @require_cr
    def create(self, bd:MultiDict, hd:Headers, cr=None):
        # Credenciais
        gc = hd.get("gc")
        
        # Dados do funcionario
        nome = bd.get("nome")
        pwd = bd.get("pwd")
        perm = bd.get("perm", "FUNC") # Confere a permissao do Funcionario
        
        if nome and pwd:
            pwdHash = sha256(pwd.encode()).hexdigest()
            new_employee = Employee()
            new_employee.nome = nome
            new_employee.hash = pwdHash
            new_employee.permissao = perm
            new_employee.cr = cr
            new_employee.grupodecliente = gc
            db.session.add(new_employee)
            db.session.commit()
            return jsonify(
                {
                    "msg": "Cadastrado com sucesso",
                    "status": "ok",
                    "matricula": new_employee.matricula
                }
            ), 200
        return jsonify('Confira os dados obrigatórios!'), 400

    @check_connection
    @require_cr
    def update(self, bd:MultiDict, hd:Headers, cr=None):
        # Credenciais 
        gc = hd.get("gc")

        # Dados
        matricula = bd.get("matricula", False)
        nome = bd.get("nome")
        perm = bd.get("perm", "FUNC")
        pwd = bd.get("pwd")

        if matricula:
            employee = Employee.query.filter_by(matricula=matricula).one()
            if employee:
                if nome: employee.nome = nome.upper()
                if perm: employee.perm = perm.upper()
                if pwd: 
                    hash = sha256(pwd.encode()).hexdigest()
                    employee.hash = hash
                db.session.commit()
                return jsonify({
                    "msg" : "Atualizado com sucesso",
                    "status": "ok",
                    "matricula": employee.matricula
                }), 200
            return jsonify("Funcionario não encontrado"), 401
        return jsonify("Matricula Obrigatória"), 400

    @check_connection
    @require_cr
    def delete(self, bd:MultiDict, hd:Headers, cr=None):
        # Id Obrigatorio
        id = bd.get("id", False)
        
        # Conferencia de Credencias e dados
        if id:
            emp = Employee.query.filter_by(id=id, cr=cr)
            if emp:
                db.session.delete(emp)
                db.session.commit()
                return jsonify("Sucesso!"), 200
        return jsonify("id obrigatório!"), 400
    