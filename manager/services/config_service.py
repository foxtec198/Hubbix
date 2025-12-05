from werkzeug.datastructures import MultiDict, Headers
from utils.safe_route import require_cr, check_connection
from utils.check_field import check_password_hash
from manager.models.employess import Employee
from manager.models.clients import Client
from manager.models.config import Config
from general.models.store import Store
from flask import jsonify
from os import path, getcwd
from utils.db import db

class ConfigService:
    @check_connection
    @require_cr
    def read(self, bd:MultiDict, hd:Headers, cr=None): # Obtem a configuração por CR
        config = Config.get(cr)
        if config: return jsonify(config.to_dict())
        return jsonify("Configuração não encontrada"), 404
    
    @check_connection
    @require_cr
    def update(self, bd:MultiDict, hd:Headers, cr=None): # Atualiza a configuração
        filter = bd.get("filter", None)
        value = bd.get("value", None)
        if filter and value:
            config = Config.get(cr)
            match filter:
                case "escala": config.escala = value
                case "estoque": config.controle_estoque = value
                case "modo_caixa": config.modo_caixa = value
                case "email": config.email_fx = value
                case "pix": config.config_pix = value
                case "peca": config.peca = value
                case "fuso": config.fuso = value
                case "nnf": config.nnf = value
                case _: return jsonify("Filtro inválido"), 400
            config.save()
            return jsonify("Configuração atualizada com sucesso")
        return jsonify("Filtro e valor são obrigatórios"), 400

    @require_cr
    @check_connection
    def update_logo(self, files, hd:Headers, cr=None): # Atualizar o arquivo de logo
        if files:
            logo_file = files.get("img")
            if logo_file:
                config = Config.get(cr)
                filename = f"{cr}.png"
                caminho = path.join(getcwd(), "manager", "assets", "img", filename)
                logo_file.save(caminho)
                config.logo = filename
                db.session.commit()
                return jsonify({
                    "msg": "Logo atualizada com sucesso",
                    "logo": filename
                }), 201
            return jsonify("Arquivo de logo não encontrado - Nome: img"), 404
        return jsonify("Upload não encontrado"), 404

    @check_connection
    def login(self, bd:MultiDict, hd:Headers): # Login
        mat = bd.get("mat")
        pwd = bd.get("pwd")

        if mat and pwd: 
            employee = Employee.query.filter_by(matricula=mat).one()
            if employee:
                if check_password_hash(pwd, employee.hash):
                    config = Config.get(employee.cr)
                    return jsonify({
                        "display_name": employee.nome,
                        "perm": employee.permissao,
                        "cr": employee.cr,
                        "gc": employee.grupodecliente,
                        "peca": config.peca,
                        "estoque": config.controle_estoque
                    })
                return jsonify("Senha Incorreta"), 401
            return jsonify("Matricula nao encontrada"), 404
        return jsonify("Matricula e Senha Obrigatorios"), 400

    @check_connection
    @require_cr
    def check_mat(self, mat, hd:Headers, cr = None):
        if mat:
            employee = Employee.query.filter_by(matricula=mat, cr=cr).first()
            if employee:
                return jsonify({
                    "display_name": employee.nome,
                    "perm": employee.permissao
                })
            return jsonify("Matricula nao encontrada"), 404
        return jsonify("Matricula obrigatoria"), 400

    @check_connection
    @require_cr
    def check_cpf(self, cpf, hd:Headers, cr = None):
        if cpf:
            client = Client.query.filter_by(cpf=cpf, cr=cr).first()
            if client:
                return jsonify({
                    "nome": client.nome,
                    "obs": client.obs
                })
            return jsonify("CPF nao encontrado"), 404
        return jsonify("CPF obrigatorio"), 400