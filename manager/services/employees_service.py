from hashlib import sha256
from flask import jsonify
from manager.models.employess import Employee, db
from werkzeug.datastructures.headers import Headers
from werkzeug.datastructures.structures import MultiDict
from utils.safe_route import require_cr, check_connection
from utils.check_field import check_field

class EmployeeService:
    @check_connection
    @require_cr
    def get(self, bd:MultiDict, cr = None):
        """
        Docstring for get
        
        :param bd: Body(Argumentos) pode ser passada a matricula (Não obrigatorio)
        :type bd: MultiDict
        :param cr: Credencial de Loja declarada no Header (Não declara na função)
        :return: (JSON, CODE)
        :rtype: tuple[Response, Literal[200]] | tuple[Response, Literal[404]]
        """
        mat = bd.get("mat") # Matricula
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
        
    @check_connection
    @require_cr
    def create(self, bd:MultiDict, hd:Headers, cr=None):
        """
        Docstring for create
        
        :param bd: Body(JSON) dados que serão utilizados para a criação do funcionario
        :type bd: MultiDict
        :param hd: Headers do request
        :type hd: Headers
        :param cr: Credencial de Loja declarada no Header (Não declara na função)
        :return: (JSON, CODE)
        :rtype: tuple[Response, Literal[201]] | tuple[Response, Literal[400]]
        """
        # ========== Dados do funcionario
        nome = bd.get("nome") # Nome
        pwd = bd.get("pwd") # Senha
        perm = bd.get("perm", "FUNC") # Permissao do Funcionario
        gc = hd.get("gc") # Grupo de Cliente
        
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

    @check_connection
    @require_cr
    def update(self, bd:MultiDict, cr=None):
        """
        Docstring for update
        
        :param bd: Body(JSON) deve ser declarado os dados a serem atualizados do cliente tendo a matricula como obrigatória
        :type bd: MultiDict
        :param cr: Credencial de Loja declarada no Header (Não declara na função)
        :return: (JSON, CODE)
        :rtype: tuple[Response, Literal[200]] | tuple[Response, Literal[404]] | tuple[Response, Literal[400]]
        """
        # ================== Dados do Funcionario
        mat = bd.get("mat") # Matricula
        nome = bd.get("nome") # Nome
        perm = bd.get("perm") # Permissao
        pwd = bd.get("pwd") # Senha

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

    @check_connection
    def delete(self, bd:MultiDict):
        """
        Docstring for delete
        
        :param bd: Parametros onde deve ser passado a matricula de forma obirgatória
        :type bd: MultiDict
        :return: (JSON, CODE)
        :rtype: tuple[Response, Literal[200]] | tuple[Response, Literal[400]]
        """
        mat = bd.get("mat") # Matricula
        if mat: # Confere se foi declarado a matricula
            db.session.delete(Employee.get(mat)) # Remove por matricula
            db.session.commit() # Salva o registro no BD
            return jsonify("Funcionario removido"), 200 # Retorna sucesso
        return jsonify("id obrigatório!"), 400 # Retorna BAD REQUEST - 400
    