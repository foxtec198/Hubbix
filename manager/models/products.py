from models.base_model import BaseModel, db
from utils.now import now, dt

class Product(BaseModel):
    __bind_key__ = "manager"
    __tablename__ = "produtos"
    
    id = db.Column(db.Integer(), primary_key=True)
    ean = db.Column(db.String(), nullable=True)
    nome = db.Column(db.String(), nullable=False)
    custo = db.Column(db.Float())    
    valor = db.Column(db.Float())    
    estoque_minimo = db.Column(db.Integer())    
    quantidade = db.Column(db.Integer())    
    desconto = db.Column(db.Float())    
    lucro = db.Column(db.Float())    
    fornecedor = db.Column(db.String(), nullable=False)    
    data = db.Column(db.DateTime(), default=dt.utcnow)
    img = db.Column(db.String())
    grupodecliente = db.Column(db.String(), nullable=False)
    cr = db.Column(db.String(), nullable=False)

    @classmethod
    def _search_by_cr(cls, cr):
        products =cls.query.filter(cls.cr==cr)
        return [prod.to_dict() for prod in products]