from general.models.base_model import BaseModel, db
from utils.now import now

class Employee(BaseModel):
    __bind_key__ = "gourmet"
    __tablename__ = "funcionarios"

    matricula = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(), nullable=False)
    hash = db.Column(db.String(), nullable=False)
    permissao = db.Column(db.String(), nullable=False)
    cr = db.Column(db.String(), nullable=False)
    grupodecliente = db.Column(db.String(), nullable=False)

    @classmethod
    def _search_by_matricula(cls, matricula):
        return cls.query.filter(cls.matricula == matricula).first()

    @classmethod
    def _search_by_cr(cls, cr):
        return [emp.to_dict() for emp in cls.query.filter(cls.cr == cr).all()]
