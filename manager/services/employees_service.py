from hashlib import sha256
from flask import jsonify
from manager.models.employess import Employee, db
from werkzeug.datastructures.headers import Headers
from werkzeug.datastructures.structures import MultiDict
from utils.check_cr import check_cr

class EmployeeService:
    def get(self, hd:Headers):
        cr = hd.get("cr", False)
        if check_cr(cr): 
            return jsonify(Employee._search_by_cr(cr)), 200
        return jsonify("Loja inexistente"), 401
        
    def create(self, bd:MultiDict, hd:Headers):
        # Credenciais
        cr = hd.get("cr", False)
        gc = hd.get("gc", False)
        
        # Dados do funcionario
        nome = bd.get("nome")
        pwd = bd.get("pwd")
        perm = bd.get("perm", "FUNC") # Confere a permissao do Funcionario
        
        if check_cr(cr): # Confere as Credenciais
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
        return jsonify('loja Inexistente'), 401

    def update(self, bd:MultiDict, hd:Headers):
        # Credenciais 
        cr = hd.get("cr", False)
        gc = hd.get("gc", False)

        # Dados
        matricula = bd.get("matricula", False)
        nome = bd.get("nome")
        perm = bd.get("perm", "FUNC")
        pwd = bd.get("pwd")

        if check_cr(cr):
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
        return jsonify("Loja Inexistente"), 401

    def delete(self, bd:MultiDict, hd:Headers):
        # Crendenciais
        cr = hd.get("cr", False)
        gc = hd.get("gc", False)

        # Id Obrigatorio
        id = bd.get("id", False)
        
        # Conferencia de Credencias e dados
        if check_cr(cr):
            if id:
                emp = Employee.query.get(id)
                db.session.delete(emp)
                db.session.commit()
            return jsonify("id obrigatório!"), 400
        return jsonify("Loja Inexistennte"), 401
    