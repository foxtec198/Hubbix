from flask import jsonify, request
from functools import wraps
from sqlalchemy.exc import OperationalError
from utils.check_cr import check_cr

def check_connection(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        try:
            return func(*args, **kwargs)
        except OperationalError as err:
            return jsonify(f"Erro operacional(Host, Internet, Db) - Erro: {err}"), 500
        except Exception as err:
            return jsonify(f"Erro Interno: {err}"), 500
    return wrapper

def require_cr(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        cr = request.headers.get("cr", None)

        if not check_cr(cr): return jsonify("Loja inexistente"), 401

        kwargs["cr"] = cr
        return func(*args, **kwargs)
    return wrapper
    