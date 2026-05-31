from general.models.base_model import BaseModel, db

class Combo(BaseModel):
    __bind_key__ = "gourmet"
    __tablename__ = "combos"

    id = db.Column(db.Integer(), primary_key=True)
    ativo = db.Column(db.Boolean(), default=True)
    grupodecliente = db.Column(db.String(), nullable=False)
    cr = db.Column(db.String(), nullable=False)

    @classmethod
    def _search_by_cr(cls, cr, gc):
        return [combo.to_dict() for combo in cls.query.filter(cls.cr == cr, cls.grupodecliente == gc).all()]

    @classmethod
    def _search_by_id(cls, id):
        return cls.query.filter(cls.id == id).first()

class ComboItem(BaseModel):
    __bind_key__ = "gourmet"
    __tablename__ = "combo_items"

    id = db.Column(db.Integer(), primary_key=True)
    quantidade = db.Column(db.Integer(), nullable=False)
    combo_id = db.Column(db.Integer(), nullable=False)
    grupodecliente = db.Column(db.String(), nullable=False)
    cr = db.Column(db.String(), nullable=False)

    @classmethod
    def _search_by_combo(cls, combo_id, cr):
        return [item.to_dict() for item in cls.query.filter(cls.combo_id == combo_id, cls.cr == cr).all()]
