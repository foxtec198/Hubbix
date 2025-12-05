from general.models.base_model import BaseModel, db
from sqlalchemy import cast, Date
from utils.now import now

class Sale(BaseModel):
    __bind_key__ = "manager"
    __tablename__ = "vendas"

    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Float)
    desconto = db.Column(db.Float)
    pagamento = db.Column(db.String)
    id_cliente = db.Column(db.Integer)
    data = db.Column(db.DateTime)
    grupodecliente = db.Column(db.String)
    cr = db.Column(db.String)
    tipo = db.Column(db.String)
    matricula = db.Column(db.Integer)
    merchant_id = db.Column(db.String)
    order_id = db.Column(db.String)
    ext_key = db.Column(db.String)
    pix_pago = db.Column(db.Boolean)
    qr = db.Column(db.String)