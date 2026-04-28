from general.models.base_model import BaseModel, db
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
    id_categoria = db.Column()

    @classmethod
    def _search_by_cr(cls, cr) -> list:
        products =cls.query.filter(cls.cr==cr)
        return [prod.to_dict() for prod in products]
        
    @classmethod
    def _search_by_name(cls, nome) -> list:
        return [prod.to_dict() for prod in cls.query.filter(cls.nome == nome).all()]

    @classmethod
    def _search_by_id(cls, id) -> dict:
        return cls.query.filter(cls.id == id).first()

    @classmethod
    def _search_by_ean(cls, ean) -> dict:
        return cls.query.filter(cls.ean == ean).first()
    
class VwProducts(BaseModel):
    __bind_key__ = "manager"
    __tablename__ = "vwprodutos"

    id = db.Column(db.Integer, primary_key=True)
    ean = db.Column(db.String)
    nome = db.Column(db.String)
    valor = db.Column(db.Float)
    quantidade = db.Column(db.Integer)
    desconto = db.Column(db.Float)
    img = db.Column(db.String)
    grupodecliente = db.Column(db.String)
    cr = db.Column(db.String)
    categoria = db.Column(db.String)
    fornecedor = db.Column(db.String)

    @classmethod
    def _searh_by_cr(prods, cr):
        products = prods.query.filter(
            prods.cr == cr
        ).order_by(
            prods.nome.asc()
        ).all()
        return [product.to_dict() for product in products]
    
    @classmethod
    def _search_by_name(prods, nome) -> list:
        products = prods.query.filter(
            prods.nome.ilike(f"%{nome}%")
        ).all()
        return [prod.to_dict() for prod in products]

    @classmethod
    def _search_by_id(prods, id) -> dict:
        return prods.query.filter(prods.id == id).first()

    @classmethod
    def _search_by_ean(prods, ean) -> dict:
        return prods.query.filter(prods.ean == ean).first()

