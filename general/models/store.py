from general.models.base_model import BaseModel
from utils.db import db, text

class Store(BaseModel):
    __bind_key__ = "lojas"
    __tablename__ = "lojas"

    cpf_cnpj = db.Column(db.String, primary_key=True)
    nome_loja = db.Column(db.String)
    data_criacao = db.Column(db.DateTime)
    bairro = db.Column(db.String)
    cep = db.Column(db.String)
    cidade = db.Column(db.String)
    estado = db.Column(db.String)
    rua = db.Column(db.String)
    pagamento = db.Column(db.String)
    negociante = db.Column(db.String)
    pacote = db.Column(db.String)
    sistema = db.Column(db.String)
    situacao = db.Column(db.String)
    grupodecliente = db.Column(db.String)
    cr = db.Column(db.String)
    mat = db.Column(db.Integer)
    teste = db.Column(db.String)
    email = db.Column(db.String)
    telefone = db.Column(db.String)
    external_pos_id = db.Column(db.String)
    user_id = db.Column(db.String)
    idloja = db.Column(db.Integer)
    ramo = db.Column(db.String)

    @classmethod
    def _search_by_cr(store, cr):
        return store.query.filter(store.cr == cr).first()
        
    @classmethod
    def check_cr(cls, cr) -> bool:
        check = Store.query.filter(Store.cr == cr).all()
        if check: return True
        else: return False
        
    @classmethod
    def get_endereco(cls, cr) -> str:
        store = Store.query.filter_by(cr=cr).one()
        if store: 
            return "%s, %s - %s %s - %s"%(store.rua, store.bairro, store.cidade, store.estado, store.cep)
        return "Endereço não localizado, favor verificar"