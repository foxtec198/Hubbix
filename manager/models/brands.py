from models.base_model import BaseModel
from utils.db import db

class Brand(BaseModel):
    __bind_key__ = "manager"
    __tablename__ = "marcas"

    id = db.Column(db.Integer(), primary_key=True)
    marca = db.Column(db.String(), nullable=False)
    cr = db.Column(db.String())
    
