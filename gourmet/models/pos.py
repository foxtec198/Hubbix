from general.models.base_model import BaseModel, db
from utils.now import dt

class POSOpen(BaseModel):
    __bind_key__ = "gourmet"
    __tablename__ = "caixa_ab"

    cr = db.Column(db.String(), primary_key=True)
    valor = db.Column(db.Float(), nullable=False)
    caixa_abertura = db.Column(db.Float(), nullable=False)
    data = db.Column(db.DateTime(), default=dt.utcnow)

    @classmethod
    def _search_by_cr(cls, cr):
        return cls.query.filter(cls.cr == cr).first()

class POSClosed(BaseModel):
    __bind_key__ = "gourmet"
    __tablename__ = "caixa_fc"

    id = db.Column(db.Integer(), primary_key=True)
    abertura = db.Column(db.Float(), nullable=False)
    fechamento = db.Column(db.Float(), nullable=False)
    grupodecliente = db.Column(db.String(), nullable=False)
    cr = db.Column(db.String(), nullable=False)
    data = db.Column(db.DateTime(), default=dt.utcnow)
    matricula = db.Column(db.Integer(), nullable=False)

    @classmethod
    def _search_by_cr(cls, cr):
        return cls.query.filter(cls.cr == cr).order_by(cls.data.desc()).first()

class POSApplied(BaseModel):
    __bind_key__ = "gourmet"
    __tablename__ = "caixa_ap"

    id = db.Column(db.Integer(), primary_key=True)
    valor = db.Column(db.Float(), nullable=False)
    valor_abertura = db.Column(db.Float(), nullable=False)
    matricula = db.Column(db.Integer(), nullable=False)
    data = db.Column(db.DateTime(), default=dt.utcnow)
