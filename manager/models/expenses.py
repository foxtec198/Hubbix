from models.base_model import BaseModel
from utils.db import db
from utils.now import dt, now, timedelta
from sqlalchemy import func, Date, cast

class Expense(BaseModel):
    __bind_key__ = "manager"
    __tablename__ = "caixa_sd"
    
    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Float)
    data = db.Column(db.DateTime, default=dt.utcnow)
    motivo = db.Column(db.String)
    matricula = db.Column(db.Integer)
    cr = db.Column(db.String)
    
    @classmethod
    def _search_by_cr(cls, cr):
        expenses = cls.query.filter_by(cr=cr)
        return [expense.to_dict() for expense in expenses]

    @classmethod
    def _search_by_date(cls, day, month, year, cr):
        months = 90 # Quantidade de meses em dias que deve ser considerada.
        if day and month and year: # Confere se foi passado os args 
            expenses = cls.query.filter(
                func.to_char(cast(cls.data, Date), 'DD-MM-YYYY') >= f"{day}-{month}-{year}",
                cls.cr == cr
            )
        else: # Caso nao tenha sido, puxa os 3 meses atuais - De acordo com a variavel "MONTHS"
            expenses = cls.query.filter(
                func.to_char(cast(cls.data, Date), 'MM-YYYY') >= (now() - timedelta(months)),
                cls.cr == cr
            )
        return [expense.to_dict() for expense in expenses]