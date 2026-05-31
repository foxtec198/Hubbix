from general.models.base_model import BaseModel, db
from utils.now import dt

class SaleExit(BaseModel):
    __bind_key__ = "gourmet"
    __tablename__ = "saidas"

    id = db.Column(db.Integer(), primary_key=True)
    id_venda = db.Column(db.Integer(), nullable=False)
    nome_produto = db.Column(db.String(), nullable=False)
    quantidade = db.Column(db.Integer(), nullable=False)
    valor = db.Column(db.Float(), nullable=False)
    funcionario = db.Column(db.Integer(), nullable=False)
    data = db.Column(db.DateTime(), default=dt.utcnow)
    cr = db.Column(db.String(), nullable=False)

    @classmethod
    def _search_by_venda(cls, id_venda, cr):
        return [exit.to_dict() for exit in cls.query.filter(cls.id_venda == id_venda, cls.cr == cr).all()]
