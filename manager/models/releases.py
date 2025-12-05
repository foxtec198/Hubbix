from general.models.base_model import BaseModel, db

class Release(BaseModel):
    __bind_key__ = "manager"
    __tablename__ = "saidas"

    id = db.Column(db.Integer, primary_key=True)
    id_venda = db.Column(db.Integer)
    nome = db.Column(db.String)
    valor = db.Column(db.Float)
    custo = db.Column(db.Float)
    data = db.Column(db.DateTime)
    cr = db.Column(db.String)
    grupodecliente = db.Column(db.String)