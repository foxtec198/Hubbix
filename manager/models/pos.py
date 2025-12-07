from general.models.base_model import BaseModel, db

class Pos(BaseModel):
    __bind_key__ = "manager"
    __tablename__ = "caixa_ab"

    cr = db.Column(db.String, primary_key=True)
    valor = db.Column(db.Float)
    data = db.Column(db.DateTime)
    abertura = db.Column(db.Float)
    matricula = db.Column(db.Integer)
    
    @classmethod
    def check(cls, cr) -> bool:
        res = Pos.query.filter_by(cr=cr).all()
        return True if res else False
    
class PosClose(BaseModel):
    __bind_key__ = "manager"
    __tablename__ = "caixa_fc"
    
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime)
    dinheiro = db.Column(db.Float)
    cartao = db.Column(db.Float)
    pix = db.Column(db.Float)
    total = db.Column(db.Float)
    saida = db.Column(db.Float)
    troco = db.Column(db.Float)
    abertura = db.Column(db.Float)
    matricula = db.Column(db.Integer)
    grupodecliente = db.Column(db.String)
    cr = db.Column(db.String)

class Items(BaseModel):
    __bind_key__ = "manager"
    __tablename__ = "md_items_caixa"

    id = db.Column(db.Integer, primary_key=True)
    id_item = db.Column(db.Integer)
    ean = db.Column(db.String)
    nome = db.Column(db.String)
    quantidade = db.Column(db.String)
    quantidade = db.Column(db.Integer)
    valor = db.Column(db.Float)
    total = db.Column(db.Float)
    cr = db.Column(db.String)
