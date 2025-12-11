from utils.db import db
from general.models.base_model import BaseModel

class Provider(BaseModel):
    __bind_key__ = "manager"
    __tablename__ = "fornecedores"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String)
    cr = db.Column(db.String)
    