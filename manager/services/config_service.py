from werkzeug.datastructures.structures import MultiDict
from werkzeug.datastructures.headers import Headers
from werkzeug.security import check_password_hash
from utils.safe_route import require_cr, check_connection
from manager.models.employess import Employee
from manager.models.config import Config
from flask import jsonify, request as rq
from hashlib import sha256

class ConfigService:
    @check_connection
    @require_cr
    def read(self, bd:MultiDict, hd:Headers, cr=None):
        config = config.get(cr)
        if config:
            return jsonify({
                "peca": config.peca,
                "logo": config.logo,
                "escala": config.escala,
                "controle_estoque": config.controle_estoque,
                "modo_caixa": config.modo_caixa,
                "email_fx": config.email_fx,
                "config_pix": config.config_pix,
                "nnf": config.nnf
            })
        return jsonify("Configuração não encontrada"), 404
    
    @check_connection
    @require_cr
    def update(self, bd:MultiDict, hd:Headers, cr=None):
        filter = bd.get("filter", None)
        value = bd.get("value", None)
        if filter and value:
            config = Config.get(cr)
            match filter:
                case "logo": config.logo = value
                case "escala": config.escala = value
                case "controle_estoque": config.controle_estoque = value
                case "modo_caixa": config.modo_caixa = value
                case "email_fx": config.email_fx = value
                case "config_pix": config.config_pix = value
                case "nnf": config.nnf = value
                case _: return jsonify("Filtro inválido"), 400
            config.save()
            return jsonify("Configuração atualizada com sucesso")
        return jsonify("Filtro e valor são obrigatórios"), 400

    @check_connection
    def login(self, bd:MultiDict, hd:Headers):
        mat = bd.get("mat")
        pwd = bd.get("pwd")

        if mat and pwd: 
            employee = Employee._search_by_mat(mat)
            if employee:
                if check_password_hash(hash, pwd):
                    config = Config.get(employee.cr)
                    return jsonify({
                        "display_name": employee.nome,
                        "perm": employee.perm,
                        "cr": employee.cr,
                        "gc": employee.gc,
                        "peca": config.peca,
                        "estoque": config.controle_estoque
                    })
                return jsonify("Senha Incorreta"), 401
            return jsonify("Matricula nao encontrada"), 404
        return jsonify("Matricula e Senha Obrigatorios"), 400