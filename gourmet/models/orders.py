from general.models.base_model import BaseModel, db
from utils.now import dt

class Order(BaseModel):
    __bind_key__ = "gourmet"
    __tablename__ = "pedidos"

    id = db.Column(db.Integer(), primary_key=True)
    id_produto = db.Column(db.Integer(), nullable=False)
    produto = db.Column(db.String(), nullable=False)
    quantidade = db.Column(db.Integer(), nullable=False)
    cmd = db.Column(db.String(), nullable=False)
    status = db.Column(db.String(), nullable=False)
    valor = db.Column(db.Float(), nullable=False)
    funcionario = db.Column(db.Integer(), nullable=False)
    data = db.Column(db.DateTime(), default=dt.utcnow)
    grupodecliente = db.Column(db.String(), nullable=False)
    cr = db.Column(db.String(), nullable=False)

    @classmethod
    def _search_by_cmd(cls, cmd, cr):
        return [order.to_dict() for order in cls.query.filter(cls.cmd == cmd, cls.cr == cr).all()]

    @classmethod
    def _search_by_id(cls, id):
        return cls.query.filter(cls.id == id).first()
