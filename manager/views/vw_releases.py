from general.models.base_model import BaseModel, db

class ViewReleases(BaseModel):
    __bind_key__ = "manager"
    __tablename__ = "vwsaidas"

    id = db.Column(db.Integer, primary_key=True)
    id_venda = db.Column(db.Integer)
    nome = db.Column(db.String)
    valor = db.Column(db.Float)
    cliente = db.Column(db.String)
    pagamento = db.Column(db.String)
    atendente = db.Column(db.String)
    data = db.Column(db.String)
    cr = db.Column(db.String)
    datam = db.Column(db.String)
    tipo = db.Column(db.String)
    qr = db.Column(db.String)
    ext_key = db.Column(db.String)
    data_dia = db.Column(db.String)
    