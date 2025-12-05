from models.base_model import BaseModel, db

class Config(BaseModel):
    __bind_key__ = "manager" # Seta o BD como Manager
    __tablename__ = "config"
    __table_args__ = {'extend_existing': True}  # <- evita erro se já existir

    cr = db.Column(db.String(), primary_key=True)
    peca = db.Column(db.Boolean(), default=False)
    logo = db.Column(db.String())
    escala = db.Column(db.Integer())
    fuso = db.Column(db.Integer())
    controle_estoque = db.Column(db.Boolean(), default=True)
    modo_caixa = db.Column(db.Boolean(), default=False)
    email_fx = db.Column(db.String(50))
    config_pix = db.Column(db.Boolean(), default=False)
    nnf = db.Column(db.Boolean(), default=True)

    @classmethod
    def get(cls, cr):
        return cls.query.filter_by(cr=cr).one()
    
    @classmethod
    def get_fuso(cls, cr):
        config = cls.query.filter_by(cr=cr).one()
        return config.fuso if config else None