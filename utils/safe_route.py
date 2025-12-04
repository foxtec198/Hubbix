from flask import jsonify, request as rq
from functools import wraps
from sqlalchemy.exc import OperationalError
from models.store_model import Store

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
        cr = rq.headers.get("cr", None)

        if not Store.check_cr(cr): return jsonify("Loja inexistente"), 401

        kwargs["cr"] = cr
        return func(*args, **kwargs)
    return wrapper
    