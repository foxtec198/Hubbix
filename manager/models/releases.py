from general.models.base_model import BaseModel, db
from datetime import datetime as dt
from utils.now import now
from dateutils import relativedelta
from manager.models.timezone import fuso

class Release(BaseModel):
    __bind_key__ = "manager"
    __tablename__ = "saidas"

    id = db.Column(db.Integer, primary_key=True)
    id_venda = db.Column(db.Integer)
    nome = db.Column(db.String)
    valor = db.Column(db.Float)
    custo = db.Column(db.Float)
    data = db.Column(db.DateTime, default=dt.now)
    cr = db.Column(db.String)
    grupodecliente = db.Column(db.String)

class ViewRelease(BaseModel):
    __bind_key__ = "manager"
    __tablename__ = "vw_saidas"

    id_saida =  db.Column(db.Integer, primary_key=True)
    id_venda =  db.Column(db.Integer)
    nome = db.Column(db.String)
    cliente = db.Column(db.String)
    valor = db.Column(db.Integer)
    pagamento = db.Column(db.String)
    atendente = db.Column(db.String)
    data = db.Column(db.DateTime)
    cr = db.Column(db.String)
    tipo = db.Column(db.String)
    qr = db.Column(db.String)
    ext_key = db.Column(db.String)


    @classmethod
    def _search_by_month(rls, month:int, cr):
        date = now(fuso(cr)) # Data Base
        init_date =  date.replace(day=1, month=month, hour=0, minute=0, second=0, microsecond=000000) # Data Inicial
        end_date =  init_date + relativedelta(months=1) - relativedelta(days=1)

        release = rls.query.filter(
            rls.cr == cr,
            rls.data >= init_date,
            rls.data < end_date
        ).all()
        
        return [s.to_dict() for s in release] # Retorna uma lista de vendas de acordo com a data selecionada
