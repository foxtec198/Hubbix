from general.models.base_model import BaseModel, db
from utils.now import dt

class Command(BaseModel):
    __bind_key__ = "gourmet"
    __tablename__ = "comandas"

    cmd = db.Column(db.String(), primary_key=True)
    valor_real = db.Column(db.Float(), nullable=False)
    funcionario = db.Column(db.Integer(), nullable=False)
    data = db.Column(db.DateTime(), default=dt.utcnow)
    cliente = db.Column(db.String())
    grupodecliente = db.Column(db.String(), nullable=False)
    cr = db.Column(db.String(), nullable=False)

    @classmethod
    def _search_by_cmd(cls, cmd, cr):
        return cls.query.filter(cls.cmd == cmd, cls.cr == cr).first()

    @classmethod
    def _search_by_cr(cls, cr):
        return [cmd.to_dict() for cmd in cls.query.filter(cls.cr == cr).all()]
