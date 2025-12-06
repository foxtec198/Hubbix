from general.models.base_model import BaseModel
from utils.db import db

class Unit(BaseModel):
    __bind_key__ = "analytics"
    __tablename__ = "units"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)