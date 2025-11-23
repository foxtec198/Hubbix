from models.base_model import BaseModel
from utils.db import db

class CashRegister(BaseModel):
    __bind_key__ = "manager"
    __tablename__ = "caixa_ab"

    cr = db.Column(db.String, primary_key=True)
    valor = db.Column(db.Float)
    data = db.Column(db.DateTime)
    abertura = db.Column(db.Float)
    matricula = db.Column(db.Integer)
    @classmethod
    def check(cls, cr) -> bool:
        res = CashRegister.query.filter_by(cr=cr).all()
        return True if res else False
    
class CashRegisterClose(BaseModel):
    __bind_key__ = "manager"
    __tablename__ = "caixa_fc"
    
    id = db.Column(db.String, primary_key=True)
    data = db.Column(db.DateTime)
    dinheiro = db.Column(db.Float)
    cartao = db.Column(db.Float)
    pix = db.Column(db.Float)
    total = db.Column(db.Float)
    saida = db.Column(db.Float)
    troco = db.Column(db.Float)
    abertura = db.Column(db.Float)
    matricula = db.Column(db.Integer)
    grupodecliente = db.Column(db.String)
    cr = db.Column(db.String)
