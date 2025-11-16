from models.base_model import BaseModel
from utils.db import db

class Sale(BaseModel):
    __bind_key__ = "manager"
    __tablename__ = "vendas"

    id = db.Column(db.Integer, primary_key=True)
    