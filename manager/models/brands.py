from models.base_model import BaseModel
from utils.db import db

class Brand(BaseModel):
    __bind_key__ = "manager"
    __tablename__ = "marcas"

    id = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(), nullable=False)
    cr = db.Column(db.String(),  nullable=False)
    
    @classmethod
    def search_by_cr(cls, cr):
        return [c.to_dict() for c in cls.query.filter_by(cr=cr).all()]