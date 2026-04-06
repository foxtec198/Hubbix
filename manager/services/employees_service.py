# Utils
from utils.safe_route import safe_route
from utils.check_field import check_field
from flask import jsonify, request as rq
from hashlib import sha256
# Models
from manager.models.employees import Employee, db

class EmployeeService:
    @safe_route
    def get(self, token_data):
        """
        ### Docstring for get employee.
        :return: (JSON, CODE)
        :rtype: tuple[Response, Literal[200]] | tuple[Response, Literal[404]]
        """

        mat = rq.args.get("mat") # Matricula
        cr = token_data.get("cr")

        if mat: # Confirma se a matricula foi declarada
            emp = Employee._search_by_mat(mat, cr) # Busca o funcionario por Matricula
            if emp: # Caso encontre da continuidade
                return jsonify({
                    "nome": emp.nome, # Nome do Funcionario
                    "matricula": emp.matricula, # Matricula
                    "perm": emp.permissao, # Permissao
                    "img": emp.photo # Nome do arquivo de foto
                }), 200 # Retorna Sucesso
            return jsonify("Funcionario nao encontrado"), 404 # Retorna NOT FOUND - 404
        return jsonify(Employee._search_by_cr(cr)), 200 # Retorna Sucesso por loja
        
    @safe_route
    def create(self, token_data):
        """
        ### Docstring for create an employee.
        
        :return: (JSON, CODE)
        :rtype: tuple[Response, Literal[201]] | tuple[Response, Literal[400]]
        """

        body = rq.get_json()

        # ========== Dados do funcionario
        nome = body.get("nome") # Nome
        pwd = body.get("pwd") # Senha
        perm = body.get("perm", "FUNC") # Permissao do Funcionario
        cr = token_data.get("cr")
        gc = token_data.get("gc")
        
        # Checa os dados obrigatorios
        ok, error = check_field(nome=nome, senha=pwd)

        if ok: # Confere se os dados obrigatorios estao OK
            pwdHash = sha256(pwd.encode()).hexdigest() # Encripta a senha para hash
            employee = Employee( # Cria um novo Funcionario
                nome = nome, hash = pwdHash,
                permissao = perm, grupodecliente = gc, 
                cr = cr
            )
            db.session.add(employee) # Adiciona o novo funcionario ao BD
            db.session.commit() # Salva os registros
            return jsonify({ "msg": "Cadastrado com sucesso", "matricula": employee.matricula }), 201 # Retorna sucesso com a matricula
        return jsonify(error), 400 # Retorna BAD REQUEST - 400

    @safe_route
    def update(self, token_data):
        """
        ### Docstring for update employee.

        :return: (JSON, CODE)
        :rtype: tuple[Response, Literal[200]] | tuple[Response, Literal[404]] | tuple[Response, Literal[400]]
        """
        body = rq.get_json()
        cr = token_data.get("cr")
        
        # ================== Dados do Funcionario
        mat = body.get("mat") # Matricula
        nome = body.get("nome") # Nome
        perm = body.get("perm") # Permissao
        pwd = body.get("pwd") # Senha

        if mat: # Confirma se foi declarado a matricula
            employee = Employee._search_by_mat(mat, cr) # Retorna o funcionario por matricula
            if employee: # Confirma se foi encontrado
                if nome: employee.nome = nome.upper() # Altera o nome se declarado
                if perm: employee.perm = perm.upper() # Altera a permissao se declarado
                if pwd: # Confirma se foi passado a senha para pode alterar
                    hash = sha256(pwd.encode()).hexdigest() # Cria o novo hash da senha
                    employee.hash = hash # Define no banco o hah alterado
                db.session.commit() # Salva os registros no Banco de Dados
                return jsonify("Funcionario atualizado"), 200 # Retorna sucesso
            return jsonify("Funcionario não encontrado"), 404 # Retorna NOT FOUND - 404
        return jsonify("Matricula Obrigatória"), 400 # Retorna BAD REQUEST - 400

    @safe_route
    def delete(self):
        """
        ### Docstring for delete employee.

        :return: (JSON, CODE)
        :rtype: tuple[Response, Literal[200]] | tuple[Response, Literal[400]]
        """
        mat = rq.args.get("mat") # Matricula
        if mat: # Confere se foi declarado a matricula
            db.session.delete(Employee.get(mat)) # Remove por matricula
            db.session.commit() # Salva o registro no BD
            return jsonify("Funcionario removido"), 200 # Retorna sucesso
        return jsonify("id obrigatório!"), 400 # Retorna BAD REQUEST - 400
    