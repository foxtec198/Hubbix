from general.models.base_model import BaseModel, db
from utils.now import dt

class Client(BaseModel):
    __bind_key__ = "manager" # Seta o BD como Manager
    __tablename__ = "clientes"
    __table_args__ = {'extend_existing': True}  # <- evita erro se já existir

    id = db.Column(db.Integer(), primary_key=True)
    cpf = db.Column(db.String()) # Add Unique = True depois
    nome = db.Column(db.String(100))
    telefone = db.Column(db.String(11))
    modelo = db.Column(db.String(100))
    marca = db.Column(db.String(100))
    cor = db.Column(db.String(100))
    endereco = db.Column(db.String(150))
    obs = db.Column(db.String(100))
    imei = db.Column(db.String(100))
    data = db.Column(db.DateTime, default=dt.utcnow)
    grupodecliente = db.Column(db.String())
    cr = db.Column(db.String())

    @classmethod
    def get_client(client, cr, id):
        return client.query.filter(client.cr == cr, client.id == id).first()

    @classmethod
    def _search_by_cpf(client, cr, cpf):
        return client.query.filter(client.cr == cr, client.cpf == id).first()

    @classmethod
    def _search_by_cr(client, cr) -> list:
        clients = client.query.filter(client.cr == cr).all()
        return [client.to_dict() for client in clients]