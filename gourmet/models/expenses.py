from general.models.base_model import BaseModel, db
from utils.now import dt

class Expense(BaseModel):
    __bind_key__ = "gourmet"
    __tablename__ = "despesas"

    id = db.Column(db.Integer(), primary_key=True)
    motivo = db.Column(db.String(), nullable=False)
    valor = db.Column(db.Float(), nullable=False)
    cr = db.Column(db.String(), nullable=False)
    grupodecliente = db.Column(db.String(), nullable=False)
    data = db.Column(db.DateTime(), default=dt.utcnow)

    @classmethod
    def _search_by_cr(cls, cr, gc):
        return [exp.to_dict() for exp in cls.query.filter(cls.cr == cr, cls.grupodecliente == gc).order_by(cls.data.desc()).all()]

    @classmethod
    def _search_by_id(cls, id):
        return cls.query.filter(cls.id == id).first()
