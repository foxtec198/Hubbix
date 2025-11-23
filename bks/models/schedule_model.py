from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from utils.db import db

class Schedule(db.Model):
    __bind_key__ = "bks"
    __tablename__ = "schedules"

    id = db.Column(db.Integer, primary_key=True)
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    data = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
