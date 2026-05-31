from general.models.base_model import BaseModel, db

class Category(BaseModel):
    __bind_key__ = "gourmet"
    __tablename__ = "categorias"

    id = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(), nullable=False)
    cr = db.Column(db.String(), nullable=False)
    grupodecliente = db.Column(db.String(), nullable=False)

    @classmethod
    def _search_by_cr(cls, cr):
        return [cat.to_dict() for cat in cls.query.filter(cls.cr == cr).all()]

    @classmethod
    def _search_by_id(cls, id):
        return cls.query.filter(cls.id == id).first()
