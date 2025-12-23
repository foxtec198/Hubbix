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
    def _search_all_by_cr(expense, cr) -> list: # Retorna todas despesas por cr
        return [e.to_dict() for e in expense.query.filter(expense.cr == cr).all()]

    @classmethod
    def _search_default(expense, cr) -> list: # Obtem por um periodo de 3 meses - padrao
        now_dt = now() # Data atual
        end_dt = now_dt.replace(day=1, hour=0, minute=0, second=0, microsecond=0) # Pega os dados referentea 3 meses atras 
        init_dt = end_dt - relativedelta(months=3)
        
        expenses = expense.query.filter( # Obtem todas as despesas de acordo com o filtro
            expense.cr == cr,
            expense.data >= init_dt,
            expense.data < end_dt
        ).order_by(
            expense.data.desc()
        ).all()

        return [e.to_dict() for e in expenses]
    
    @classmethod
    def _search_all_by_date(expense, cr, dt=now()) -> list: # Obtem por um periodo especifico
        dt = dt.replace(day=dt.day, month=dt.month, year=dt.year, hour=0, minute=0, second=0, microsecond=0) # Transforma a data em DD-MM-YYYY 00:00:00:000
        end_dt = dt.replace(hour=23, minute=59, second=59) # Trasnforma no final do di - DD-MM-YYYY 23:59:59

        # Obtem todas as depesas pela data
        expenses = expense.query.filter(
            expense.cr == cr, 
            expense.data >= dt, 
            expense.data < end_dt
        ).order_by(
            expense.data.desc()
        ).all()

        # Retorna as despesas
        return [e.to_dict() for e in expenses] 
        
    
    @classmethod
    def _search_by_id(expense, cr, id):
        return expense.query.filter(expense.cr == cr, expense.id == id).first()

    @classmethod
    def get_expense(expense, id, cr) -> dict: # Obtem por id
        # Seleciona por ID e por CR - Quase uma autenticação de dois fatores rs.
        e = expense.query.filter(expense.cr == cr, expense.id == id).first() 
        
        # O motivo de pegar o FIRST e nao o ONE, é que se não obtiver resultado no FIRST ele retorna vazio, já o ONE retorna erro.
        return e.to_dict() # Retorna as despesas