from general.models.base_model import BaseModel, db
from utils.now import dt, now
from dateutil.relativedelta import relativedelta

class Expense(BaseModel):
    __bind_key__ = "manager" # Banco de dados
    __tablename__ = "caixa_sd" # Tabela
    
    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Float)
    data = db.Column(db.DateTime, default=dt.utcnow)
    motivo = db.Column(db.String)
    matricula = db.Column(db.Integer)
    cr = db.Column(db.String)
    
    @classmethod
    def _search_all_by_cr(self, cr) -> list: # Retorna todas despesas por cr
        return [expense.to_dict() for expense in self.query.filter_by(cr=cr).all()]

    @classmethod
    def _search_default(self, cr) -> list: # Obtem por um periodo de 3 meses - padrao
        now_dt = now() # Data atual
        end_dt = now_dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0) # Pega os dados referentea 3 meses atras 
        init_dt = end_dt - relativedelta(months=3)
        
        expenses = self.query.filter( # Obtem todas as despesas de acordo com o filtro
            self.cr == cr,
            self.data >= init_dt,
            self.data < end_dt
        ).order_by(
            self.data.desc()
        ).all()

        return [expense.to_dict() for expense in expenses]
    
    @classmethod
    def _search_all_by_date(self, cr, dt=now()) -> list: # Obtem por um periodo especifico
        dt = dt.replace(day=dt.day, month=dt.month, year=dt.year, hour=0, minute=0, second=0, microsecond=0) # Transforma a data em DD-MM-YYYY 00:00:00:000
        end_dt = dt.replace(hour=23, minute=59, second=59) # Trasnforma no final do di - DD-MM-YYYY 23:59:59

        # Obtem todas as depesas pela data
        expenses = self.query.filter(self.data >= dt, self.data < end_dt).all()

        # Retorna as despesas
        return [expense.to_dict() for expense in expenses] 
    
    @classmethod
    def get_expense(self, id, cr) -> dict: # Obtem por id
        # Seleciona por ID e por CR - Quase uma autenticação de dois fatores rs.
        expense = self.query.filter(self.cr == cr, self.id == id).first() 
        
        # O motivo de pegar o FIRST e nao o ONE, é que se não obtiver resultado no FIRST ele retorna vazio, já o ONE retorna erro.
        return expense.to_dict() # Retorna as despesas