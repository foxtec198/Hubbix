from general.models.base_model import BaseModel, db
from utils.now import dt, now
from dateutil.relativedelta import relativedelta
from manager.models.employees import Employee

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
        init_dt = now_dt - relativedelta(months=3)
        
        # Obtem todas as despesas de acordo com o filtro
        expenses = db.session.query(
            expense.id,
            expense.motivo,
            expense.valor,
            expense.data,
            Employee.nome.label("funcionario"),
            Employee.photo
        ).join(
            Employee, Employee.matricula == expense.matricula
        ).filter( 
            expense.cr == cr,
            expense.data >= init_dt,
            expense.data < now_dt
        ).order_by(
            expense.data.desc()
        ).all()
        
        res = list()
        for e in expenses:
            res.append({
                "id": e.id,
                "motivo": e.motivo,
                "valor": e.valor,
                "data": e.data,
                "funcionario": e.funcionario,
                "photo": e.photo
            })
            
        return res
            
    
    @classmethod
    def _search_all_by_date(expense, cr, dt=now()) -> list: # Obtem por um periodo especifico
        dt = dt.replace(day=dt.day, month=dt.month, year=dt.year, hour=0, minute=0, second=0, microsecond=0) # Transforma a data em DD-MM-YYYY 00:00:00:000
        end_dt = dt.replace(hour=23, minute=59, second=59) # Trasnforma no final do di - DD-MM-YYYY 23:59:59

        expenses = db.session.query(
            expense.id,
            expense.motivo,
            expense.valor,
            expense.data,
            Employee.nome.label("funcionario"),
            Employee.photo
        ).join(
            Employee, Employee.matricula == expense.matricula
        ).filter( 
            expense.cr == cr, 
            expense.data >= dt, 
            expense.data < end_dt
        ).order_by(
            expense.data.desc()
        ).all()
        
        res = list()
        for e in expenses:
            res.append({
                "id": e.id,
                "motivo": e.motivo,
                "valor": e.valor,
                "data": e.data,
                "funcionario": e.funcionario,
                "photo": e.photo
            })
        return res
        
    
    @classmethod
    def _search_by_id(expense, cr, id):
        expenseSearch = db.session.query(
            expense.id,
            expense.motivo,
            expense.valor,
            expense.data,
            Employee.nome.label("funcionario"),
            Employee.photo
        ).join(
            Employee, Employee.matricula == expense.matricula
        ).filter( 
            expense.cr == cr,
            expense.id == id
        ).order_by(
            expense.data.desc()
        ).first()

        res = list()
        for e in expenseSearch:
            res.append({
                "id": e.id,
                "motivo": e.motivo,
                "valor": e.valor,
                "data": e.data,
                "funcionario": e.funcionario,
                "photo": e.photo
            })
        return res
