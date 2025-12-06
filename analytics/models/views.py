from general.models.base_model import BaseModel
from utils.db import db

class View(BaseModel):
    __bind_key__ = "analytics"
    __tablename__ = "views"

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String)
    unit_id = db.Column(db.Integer)
    client_id = db.Column(db.Integer)
    date = db.Column(db.DateTime)
    ip = db.Column(db.String)