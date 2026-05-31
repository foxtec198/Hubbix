from general.models.base_model import BaseModel, db
from utils.now import dt

class Product(BaseModel):
    __bind_key__ = "gourmet"
    __tablename__ = "produtos"

    id = db.Column(db.Integer(), primary_key=True)
    sku = db.Column(db.String())
    nome = db.Column(db.String(), nullable=False)
    id_categoria = db.Column(db.Integer(), nullable=False)
    custo = db.Column(db.Float())
    valor = db.Column(db.Float(), nullable=False)
    quantidade = db.Column(db.Integer(), default=0)
    alerta = db.Column(db.String())
    preparo = db.Column(db.Boolean(), default=False)
    img = db.Column(db.String(), default='blank.png')
    data = db.Column(db.DateTime(), default=dt.utcnow)
    cr = db.Column(db.String(), nullable=False)
    grupodecliente = db.Column(db.String(), nullable=False)

    @classmethod
    def _search_by_cr(cls, cr):
        return [prod.to_dict() for prod in cls.query.filter(cls.cr == cr).all()]

    @classmethod
    def _search_by_id(cls, id):
        return cls.query.filter(cls.id == id).first()

    @classmethod
    def _search_by_nome(cls, nome):
        return [prod.to_dict() for prod in cls.query.filter(cls.nome.ilike(f"%{nome}%")).all()]
