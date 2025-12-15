from utils.db import db
from general.models.base_model import BaseModel

class Provider(BaseModel):
    __bind_key__ = "manager" # banco de dados
    __tablename__ = "fornecedores" # Tabela

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    nome = db.Column(db.String, nullable=False) # Nome do Forn.
    telefone = db.Column(db.String, nullable=True) # Telefone
    cr = db.Column(db.String, nullable=False) # "ID" da Loja
    grupodecliente = db.Column(db.String, nullable=False) # "ID" do Grupo de Cliente

    @classmethod
    def get_provider(provider, cr, id) -> dict:
        provider.query.filter( # Obtem um fornecedor em especifico de acordo com id e o cr
            provider.cr == cr,
            provider.id == id
        ).first()
        return provider
    
    @classmethod
    def _search_by_cr(provider, cr) -> list:
        # Obtem os fornecedores de acordo com a loja (CR)
        providers = provider.query.filter(provider.cr == cr).all()

        # Retorna uma lista de fornecedores por loja 
        return [prov.to_dict() for prov in providers]

    