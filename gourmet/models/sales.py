from general.models.base_model import BaseModel, db
from utils.now import dt

class Sale(BaseModel):
    __bind_key__ = "gourmet"
    __tablename__ = "vendas"

    id = db.Column(db.Integer(), primary_key=True)
    cmd = db.Column(db.String(), nullable=False)
    valor_real = db.Column(db.Float(), nullable=False)
    valor_pago = db.Column(db.Float(), nullable=False)
    cliente = db.Column(db.String())
    grupodecliente = db.Column(db.String(), nullable=False)
    cr = db.Column(db.String(), nullable=False)
    data = db.Column(db.DateTime(), default=dt.utcnow)
    status = db.Column(db.String(), default='FINALIZADA')
    debito = db.Column(db.Float(), default=0)
    credito = db.Column(db.Float(), default=0)
    pix = db.Column(db.Float(), default=0)
    dinheiro = db.Column(db.Float(), default=0)
    desconto = db.Column(db.Float(), default=0)
    troco = db.Column(db.Float(), default=0)
    funcionario = db.Column(db.Integer(), nullable=False)

    @classmethod
    def _search_by_cr(cls, cr):
        return [sale.to_dict() for sale in cls.query.filter(cls.cr == cr).order_by(cls.data.desc()).all()]

    @classmethod
    def _search_by_id(cls, id):
        return cls.query.filter(cls.id == id).first()
