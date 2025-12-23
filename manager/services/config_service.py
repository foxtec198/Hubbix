from werkzeug.datastructures import MultiDict, Headers
from utils.safe_route import require_cr, check_connection
from utils.check_field import check_password_hash
from manager.models.employees import Employee
from manager.models.clients import Client
from manager.models.config import Config
from general.models.store import Store
from flask import jsonify, request as rq
from os import path, getcwd
from utils.db import db
from utils.check_field import check_field

class ConfigService:
    @check_connection
    @require_cr
    def read(self, cr = None) -> tuple:
        """
        Docstring for read
        
        :param cr: Credencial de Loja declarado no Header (Não declarara na função!)
        :return: (JSON, CODE)
        :rtype: tuple[Response, Literal[200]] | tuple[Response, Literal[404]]
        """
        config = Config.get(cr) # Busca a config por CR
        if config: return jsonify(config.to_dict()), 200 # Retorna Sucesso e a lista de configuração
        return jsonify("Configuração não encontrada"), 404 # Retorna NOT FOUND - 404
    
    @check_connection
    @require_cr
    def update(self, bd:MultiDict, cr=None) -> tuple:
        """
        Docstring for update
        
        :param bd: Body(JSON) necessário dois campos (filter, value)
        :param type: MultiDict
        :param cr: Credencial de Loja declarado no Header (Não declarara na função!)
        :return: (JSON, CODE)
        :rtype: tuple[Response, Literal[200]] | tuple[Response, Literal[400]]
        """
        filter = bd.get("filter") # Filtro da config a ser atualizada!
        value = bd.get("value") # Valor a ser atualizado

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
            return jsonify("Configuração atualizada"), 200 # Retorna Sucesso
        return jsonify("Filtro e valor são obrigatórios"), 400 # Retorna BAD REQUEST - 400

    @require_cr
    @check_connection
    def update_logo(self, cr=None) -> tuple:
        """
        Docstring for update_logo
        
        :param cr: Credencial de Loja declarado no Header (Não declarara na função!)
        :return: (JSON, CODE)
        :rtype: tuple[Response, Literal[201]] | tuple[Response, Literal[404]]
        """
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

    @check_connection
    def login(self, bd:MultiDict) -> tuple:
        """
        Docstring for login
        
        :param bd: Body(JSON) onde deve ser enviado a Matricula e Senha
        :param type: MultiDict
        :return: (JSON, CODE)
        :rtype: tuple[Response, Literal[200]] | tuple[Response, Literal[404]] | tuple[Response, Literal[401]] tuple[Response, Literal[400]]
        
        """
        mat = bd.get("mat") # Matricula
        pwd = bd.get("pwd") # Senha

        # Checka os dados obrigatórios
        ok, error = check_field(matricula=mat, senha=pwd)

        if ok: # Caso os dados estejam OK da continuidade
            employee = Employee.query.filter_by(matricula=mat).first() # Busca o funcionario por matricula
            if employee: # Caso encontre 
                if check_password_hash(pwd, employee.hash): # Checka o hash do password com o do BD
                    config = Config.get(employee.cr) # Busca as configurações da loja
                    return jsonify({
                        "display_name": employee.nome, # Nome do Funcionario
                        "perm": employee.permissao, # Permisssão
                        "cr": employee.cr, # CR
                        "gc": employee.grupodecliente, # Grupo de Cliente (gc)
                        "peca": config.peca, # Config Rapida - Controle de Peças
                        "estoque": config.controle_estoque # Config Rapida - Controle de Estoque
                    }), 200 # Retorna sucesso com os dados
                return jsonify("Senha incorreta"), 401 # Retorna UNAUTHORIZED - 401
            return jsonify("Matricula não encontrada"), 404 # Retorna NOT FOUND - 404
        return jsonify(error), 400 # Retorna BAD REQUEST - 400

    @check_connection
    @require_cr
    def check_mat(self, mat:int, cr = None) -> tuple:
        """
        Docstring for check_mat \n
        Está função serve para realizar a checagem de matricula depois de logado, normalmente utilizada para funções administrativas e para checagem de permissão

        :param mat: Matricula que deve ser declarada como parametro na URL
        :param type: Integer - int()
        :param cr: Credencial de Loja declarado no Header (Não declarara na função!)
        :return: (JSON, CODE)
        :rtype: tuple[Response, Literal[200]] | tuple[Response, Literal[404]] | tuple[Response, Literal[400]]
        """
        if mat: # Confere se foi declarado a matricula
            employee = Employee._search_by_mat(mat, cr) # Busca o funcionario por MAT
            if employee: return jsonify({ "display_name": employee.nome, "perm": employee.permissao }), 200 # Retorna sucesso com nome e perm
            return jsonify("Matricula nao encontrada"), 404 # Retorna NOT FOUND - 404
        return jsonify("Matricula é obrigatória"), 400 # Retorna BAD REQUEST - 400

    @check_connection
    @require_cr
    def check_cpf(self, cpf:str, cr = None) -> tuple:
        """
        Docstring for check_cpf - Usado para confirmar se o cliente tem alguma OBS em seu cpf

        :param cpf: Deve ser passado como parametro na URL
        :param type: String - str()
        :param cr: Credencial de Loja declarado no Header (Não declarara na função!)
        ;return: (JSON, CODE)
        :rtype: tuple[Response, Literal[200]] | tuple[Response, Literal[404]] | tuple[Response, Literal[400]]
        """
        if cpf: # Confirma se foi declarado o CPF
            client = Client._search_by_cpf(cr, cpf) # Busca o cliente por CPF            
            if client: return jsonify({ "nome": client.nome, "obs": client.obs }), 200 # Retorna Sucesso
            return jsonify("CPF nao encontrado"), 404 # Retorna NOT FOUND - 404
        return jsonify("CPF obrigatorio"), 400 # Retorna BAD REQUEST - 400