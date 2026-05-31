from hashlib import sha256
from flask import jsonify, request as rq
from gourmet.models.employees import Employee
from gourmet.models.config import Config
from utils.token import create_token
from utils.check_field import check_password_hash

class AuthService:
    def login(self):
        body = rq.get_json()
        matricula = body.get('mat')
        password = body.get('pwd')

        # Confere se matricula e senha foram passados
        if not matricula or not password: return jsonify({'error': 'Matrícula e senha são obrigatórias'}), 400

        # Obtem o funcionario do BD
        employee = Employee._search_by_matricula(matricula)

        # Confirma se foi encontrado
        if not employee: return jsonify({'error': 'Matrícula incorreta'}), 401

        # Confirma se o hash está correto
        if not check_password_hash(password, employee.hash): return jsonify({'error': 'Senha incorreta'}), 401

        # Obtem a config
        config = Config._search_by_cr(employee.cr)

        # Cria o dicionario com os dados do func
        data = {
            'mat': matricula, 
            'display_name': employee.nome.split()[0], 
            'perm': employee.permissao, 
            'cr': employee.cr, 
            'gc': employee.grupodecliente,
        }

        # Cria o token de acesso
        token = create_token(data)
        if not token: return jsonify({"Error": "Erro ao criar token"}), 500

        # Inclui na response o token e a config
        data["access_token"] = token
        data["config"] =  config.to_dict() if config else {}
        
        # Retorno final
        return jsonify(data), 200
