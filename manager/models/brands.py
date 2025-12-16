from general.models.base_model import BaseModel, db

class Brand(BaseModel):
    __bind_key__ = "manager"
    __tablename__ = "marcas"

    id = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(), nullable=False)
    cr = db.Column(db.String(),  nullable=False)
    
    @classmethod
    def _search_by_cr(brand, cr) -> list:
        return [b.to_dict() for b in brand.query.filter(brand.cr == cr).all()]

    @classmethod
    def get_brand(brand, cr, id) -> list:
        return brand.query.filter(brand.cr == cr, brand.id == id).first()