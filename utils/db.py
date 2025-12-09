# db_manager.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text, create_engine
from os import environ

db = SQLAlchemy()

def cons(sql, *args, db="MANAGER", all=True):
    """db deve receveber ["MANAGER", "GOURMET", "LOJAS", "ANALYTICS"]"""
    dbs = ["MANAGER", "GOURMET", "LOJAS", "ANALYTICS"]
    if db.upper() in dbs: 
        engine = create_engine(environ[db])
        with engine.connect() as conn:
            if len(args) == 1: args = args[0]
            txt = sql % args
            res = conn.execute(text(txt))
            res = res.fetchall()
            if len(res) == 1 and not all: return list(res[0]) # Verifica se há somente um valor e o retorna apenas !
            else:
                # A resposta dos valores internos é uma tupla, e nao pode ser convertida para JSON
                # Por isso convertemos internamente para uma lista
                ls = []
                for item in res: ls.append(list(item))
                return ls
    return False

def query(sql, *args, db="MANAGER"):
    """db deve receveber ["MANAGER", "GOURMET", "LOJAS", "ANALYTICS"]"""
    if type(db) == str and db:
        engine = create_engine(environ[db])
        with engine.connect() as conn:
            if len(args) == 1: args = args[0]
            txt = sql % args
            res = conn.execute(text(txt))
            conn.commit()
            try:
                res = res.fetchall()
                if len(res) == 1: return list(res[0]) # Verifica se há somente um valor e o retorna apenas !
                else:
                    # A resposta dos valores internos é uma tupla, e nao pode ser convertida para JSON
                    # Por isso convertemos internamente para uma lista
                    ls = []
                    for item in res: ls.append(list(item))
                    return ls
            except: return 'Sem retorno da Query!'
    return False