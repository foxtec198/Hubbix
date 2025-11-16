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
