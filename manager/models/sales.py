from general.models.base_model import BaseModel, db

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

    @classmethod
    def _search_by_cr(sale, cr): # Retorna as vendas por cr
        return [s.to_dict() for s in sale.query.filter(sale.cr==cr).all()]

    @classmethod
    def _search_by_id(sale, id): # Retorna as vendas por id
        return sale.query.filter(sale.id==id).first()