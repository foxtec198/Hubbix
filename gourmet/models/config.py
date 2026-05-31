from general.models.base_model import BaseModel, db

class Config(BaseModel):
    __bind_key__ = "gourmet"
    __tablename__ = "config"

    cr = db.Column(db.String(), primary_key=True)
    imprimir = db.Column(db.Boolean(), default=False)
    pedidos = db.Column(db.Boolean(), default=False)
    comandas = db.Column(db.Boolean(), default=False)
    estoque = db.Column(db.Boolean(), default=False)
    combos = db.Column(db.Boolean(), default=False)
    fuso = db.Column(db.String(), default='UTC')
    email = db.Column(db.String())
    logo = db.Column(db.String())

    @classmethod
    def _search_by_cr(cls, cr):
        return cls.query.filter(cls.cr == cr).first()
