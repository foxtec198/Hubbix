from models.base_model import BaseModel
from utils.db import db
from utils.now import dt
from sqlalchemy import cast, Date, func

class vwOS(BaseModel):
    __bind_key__ = "manager"
    __tablename__ = "vwos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String)
    modelo = db.Column(db.String)
    marca = db.Column(db.String)
    valor = db.Column(db.Float)
    situacao = db.Column(db.String)
    atendente = db.Column(db.String)
    entrega = db.Column(db.DateTime(), default=dt.utcnow)
    abertura = db.Column(db.DateTime(), default=dt.utcnow)
    tipo = db.Column(db.String)
    cpf = db.Column(db.String)
    imei = db.Column(db.String)
    cor = db.Column(db.String)
    cr = db.Column(db.String)

    @classmethod
    def search_by_cr(cls, cr):
        o = []
        oss = cls.query.filter_by(cr=cr).all()
        for os in oss: o.append(os.to_dict())
        return o

    @classmethod
    def search_by_status(cls, status:str, cr):
        o = []
        oss = cls.query.filter_by(cr=cr, situacao=status).all()
        for os in oss: o.append(os.to_dict())
        return o

    @classmethod
    def get_expireds(cls, cr, data):
        expireds = []

        oss = vwOS.query
        oss = oss.filter(
            vwOS.cr == cr,
            vwOS.situacao.in_(["ABERTA", "ORÇAMENTO"]),
            func.to_char(cast(vwOS.abertura, Date), 'MM-YYYY') >= data
        ).order_by(vwOS.abertura.desc()).all()

        for os in oss: expireds.append(os.to_dict())
        return expireds
        

        
    