from general.models.base_model import BaseModel
from utils.db import db

class User(BaseModel):
    __bind_key__ = "analytics"
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    email = db.Column(db.String)
    hash = db.Column(db.LargeBinary)
    unit_id = db.Column(db.Float)