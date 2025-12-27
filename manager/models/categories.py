from general.models.base_model import BaseModel, db

class Categorie(BaseModel):
    __bind_key__ = "manager"
    __tablename__ = "categorias"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String)
    cr = db.Column(db.String)
    gc = db.Column(db.String)

    @classmethod
    def _search_by_cr(categorie, cr):
        categories = categorie.query.filter(
            categorie.cr == cr
        ).order_by(
            categorie.nome.asc()
        ).all()
        
        return [c.to_dict() for c in categories]

    @classmethod
    def _seach_by_id(categorie, id, cr):
        return categorie.query.filter_by(cr=cr, id=id).first()