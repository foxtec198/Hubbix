from general.models.base_model import BaseModel
from utils.db import db

class Part(BaseModel):
    __bind_key__ = "manager"
    __tablename__ = "pecas"

    id = db.Column(db.Integer, primary_key=True)