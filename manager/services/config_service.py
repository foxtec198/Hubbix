# Utils
from utils.safe_route import safe_route
from utils.check_field import check_password_hash
from utils.check_field import check_field
from utils.token import create_token
from flask import jsonify, request as rq
from os import path, getcwd
# Models
from manager.models.employees import Employee, db
from manager.models.clients import Client
from manager.models.config import Config

class ConfigService:
    def login(self) -> tuple:
        """
        ### Docstring for login.
        Function used to Login in the system and obtain the access token.
        
        :return: (JSON, CODE)
        :rtype: tuple[Response, Literal[200]] | tuple[Response, Literal[404]] | tuple[Response, Literal[401]] tuple[Response, Literal[400]]
        """

        body = rq.get_json() # Obtem o JSON do Body
        mat = body.get("mat") # Matricula
        pwd = body.get("pwd") # Senha

        # Checka os dados obrigatórios
        ok, error = check_field(matricula=mat, senha=pwd)

        if ok: # Caso os dados estejam OK da continuidade
            employee = Employee.query.filter_by(matricula=mat).first() # Busca o funcionario por matricula
            if employee: # Caso encontre 
                if check_password_hash(pwd, employee.hash): # Checka o hash do password com o do BD
                    token = create_token({ "cr": employee.cr, "gc": employee.grupodecliente }) # Cria o token com os dados
                    return jsonify({"access_token": token, "display_name": employee.nome, "perm": employee.permissao, "mat": employee.matricula }), 200 # Retorna sucesso com os dados
                return jsonify("Senha incorreta"), 401 # Retorna UNAUTHORIZED - 401
            return jsonify("Matricula não encontrada"), 404 # Retorna NOT FOUND - 404
        return jsonify(error), 400 # Retorna BAD REQUEST - 400
    
    @safe_route
    def read(self, token_data) -> tuple:
        """
        Docstring for read
        
        :param cr: Credencial de Loja declarado no Header (Não declarara na função!)
        :return: (JSON, CODE)
        :rtype: tuple[Response, Literal[200]] | tuple[Response, Literal[404]]
        """
        cr = token_data.get("cr") # Obtém o CR do Token
        config = Config.get(cr) # Busca a config por CR
        if config: return jsonify(config.to_dict()), 200 # Retorna Sucesso e a lista de configuração
        return jsonify("Configuração não encontrada"), 404 # Retorna NOT FOUND - 404
    
    @safe_route
    def update(self, token_data) -> tuple:
        """
        Docstring for update
        
        :param bd: Body(JSON) necessário dois campos (filter, value)
        :param type: MultiDict
        :param cr: Credencial de Loja declarado no Header (Não declarara na função!)
        :return: (JSON, CODE)
        :rtype: tuple[Response, Literal[200]] | tuple[Response, Literal[400]]
        """
        cr = token_data.get("cr") # Obtém o cr do token
        body = rq.get_json() # Obtem o JSON do Body
        filter = body.get("filter") # Filtro da config a ser atualizada!
        value = body.get("value") # Valor a ser atualizado

        if filter and value: # Confirma a presença de ambos
            config = Config.get(cr) # Busca a config atual
            match filter: # Compara o filter usando o match
                case "escala": config.escala = value
                case "estoque": config.controle_estoque = value
                case "modo_caixa": config.modo_caixa = value
                case "email": config.email_fx = value
                case "pix": config.config_pix = value
                case "peca": config.peca = value
                case "fuso": config.fuso = value
                case "nnf": config.nnf = value
                case _: return jsonify("Filtro inválido"), 400 # Retorna BAD REQUEST - 400
            db.session.commit() # Salva os dados no Banco
            return jsonify("Configuração atualizada"), 200 # Retorna Sucesso - 200
        return jsonify("Filtro e valor são obrigatórios"), 400 # Retorna BAD REQUEST - 400

    @safe_route
    def update_logo(self, token_data) -> tuple:
        """
        ### Docstring for update_logo.
        Use for update the store logo.

        :rtype: tuple[Response, Literal[201]] | tuple[Response, Literal[404]]
        """
        cr = token_data.get("cr")
        files = rq.files # Obtem os arquivos do Request
        if files: # Confirma se foi declarado o FILES
            logo_file = files.get("img") # Busca pelo arquivo chamado IMG
            if logo_file: # Caso encontre da procedimento
                config = Config.get(cr) # Obtem a config por cr
                if config:
                    filename = f"{cr}.png" # Define o nome da imagem
                    caminho = path.join(getcwd(), "manager", "assets", "img", filename) # Define o caminho seguro pra imagem
                    logo_file.save(caminho) # Salva localmente o arquivo
                    config.logo = filename # Seta o FILENAME da logo na loja
                    db.session.commit() # Salva as alterações
                    return jsonify({ "msg": "Logo atualizada", "logo": filename }), 201 # Retorna CREATED - 201
                return jsonify("Configuração não encontrada"), 404 # Retorna NOT FOUND - 404
            return jsonify("Arquivo de logo não encontrado - Nome: img"), 404 # Retorna NOT FOUND - 404
        return jsonify("Upload não encontrado"), 404 # Retorna NOT FOUND - 404

    @safe_route
    def check_mat(self, mat:int, token_data) -> tuple:
        """
        Docstring for check_mat \n
        Está função serve para realizar a checagem de matricula depois de logado, normalmente utilizada para funções administrativas e para checagem de permissão

        :param mat: Matricula que deve ser declarada como parametro na URL
        :param type: Integer - int()
        :rtype: tuple[Response, Literal[200]] | tuple[Response, Literal[404]] | tuple[Response, Literal[400]]
        """

        cr = token_data.get("cr") # Obtém o CR do token
        if mat: # Confere se foi declarado a matricula
            employee = Employee._search_by_mat(mat, cr) # Busca o funcionario por MAT
            if employee: return jsonify({ "display_name": employee.nome, "perm": employee.permissao }), 200 # Retorna sucesso com nome e perm
            return jsonify("Matricula nao encontrada"), 404 # Retorna NOT FOUND - 404
        return jsonify("Matricula é obrigatória"), 400 # Retorna BAD REQUEST - 400

    @safe_route
    def check_cpf(self, cpf:str, token_data) -> tuple:
        """
        Docstring for check_cpf - Usado para confirmar se o cliente tem alguma OBS em seu cpf

        :param cpf: Deve ser passado como parametro na URL
        :param type: String - str()
        :rtype: tuple[Response, Literal[200]] | tuple[Response, Literal[404]] | tuple[Response, Literal[400]]
        """
        if cpf: # Confirma se foi declarado o CPF
            cr = token_data.get("cr") # Obtém o CR do token
            client = Client._search_by_cpf(cr, cpf) # Busca o cliente por CPF            
            if client: return jsonify({ "nome": client.nome, "obs": client.obs }), 200 # Retorna Sucesso
            return jsonify("CPF nao encontrado"), 404 # Retorna NOT FOUND - 404
        return jsonify("CPF obrigatorio"), 400 # Retorna BAD REQUEST - 400