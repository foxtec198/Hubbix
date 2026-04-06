from flask import jsonify, request as rq
from functools import wraps
from general.models.store import Store
from jwt import decode, ExpiredSignatureError
import inspect

def safe_route(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        access_token = rq.headers.get("Access-Token") # Obtem o token do Header
        if not access_token: return jsonify("Token de acesso obrigatorio"), 400 # Caso não encontre, retorna BAD REQUEST
        if not Store.check_cr(access_token.get("cr")): return jsonify("Loja inexistente"), 401
        try: # Teste de token
            sig = inspect.signature(func) # Ontem a assinatura da função
            if "token_data" in sig.parameters: # Confirma se o token_data foi passado
                token_data = decode(access_token) # Obtem os dados do JWT Token depois dedescriptografar
                kwargs["token_data"] = token_data # Adiciona os dados do token no Kwargs
            return func(*args, **kwargs) # Retorna a função e seus params
        except ExpiredSignatureError: return jsonify("Token de acesso expirado"), 401 # Retorna token expirado 401 UNAUTHORIZED
        except Exception as e: return jsonify("Erro com o servidor: " + str(e)), 500 # Retorna invalido 401 UNAUTHORIZED
    return wrapper # Retorna o wrapper
    