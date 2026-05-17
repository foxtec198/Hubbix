from general.models.base_model import BaseModel, db
from utils.now import dt

class Order(BaseModel):
    __bind_key__ = "manager"
    __tablename__ = "os"

    id = db.Column(db.Integer(), primary_key=True)
    id_cliente = db.Column(db.Integer(), nullable=False)
    modelo = db.Column(db.String(50), nullable=False)
    cor = db.Column(db.String(50), nullable=False)
    marca = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    obs = db.Column(db.String(50))
    relato = db.Column(db.String(50))
    entrega = db.Column(db.DateTime(50), default=dt.utcnow)
    abertura = db.Column(db.DateTime(50), default=dt.utcnow)
    ligar = db.Column(db.Boolean(), nullable=False, default=True)
    situacao = db.Column(db.String())
    valor = db.Column(db.Float())
    atendente = db.Column(db.String())
    arquivo = db.Column(db.String())
    custo = db.Column(db.Float())
    pagamento = db.Column(db.String())
    valor_pecas = db.Column(db.Float())
    grupodecliente = db.Column(db.String(), nullable=False)
    cr = db.Column(db.String(), nullable=False)
    imei = db.Column(db.String())

    @classmethod
    def _search_by_cr(cls, cr):
        oss = cls.query.filter(cls.cr==cr).all()
        return [o.to_dict() for o in oss]

    @classmethod
    def _search_by_id(cls, id):
        oss = cls.query.filter(cls.id == id).all()
        return [o.to_dict() for o in oss]
    

        

        
    