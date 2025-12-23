from general.models.base_model import BaseModel, db
from manager.models.timezone import fuso
from manager.models.employees import Employee
from utils.now import now

class Sale(BaseModel):
    __bind_key__ = "manager"
    __tablename__ = "vendas"

    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Float)
    desconto = db.Column(db.Float)
    pagamento = db.Column(db.String)
    id_cliente = db.Column(db.Integer)
    data = db.Column(db.DateTime)
    grupodecliente = db.Column(db.String)
    cr = db.Column(db.String)
    tipo = db.Column(db.String)
    matricula = db.Column(db.Integer)
    merchant_id = db.Column(db.String)
    order_id = db.Column(db.String)
    ext_key = db.Column(db.String)
    pix_pago = db.Column(db.Boolean)
    qr = db.Column(db.String)
    
    @classmethod
    def _search_by_date(sale, day:int, month:int, year:int, cr):
        date = now(fuso(cr)) # Data Base
        init_date =  date.replace(day=day, month=month, year=year, hour=0, minute=0, second=0, microsecond=000000) # Data Inicial
        end_date =  date.replace(day=day, month=month, year=year, hour=23, minute=59, second=59, microsecond=999999) # Data Fianl
        sales = sale.query( # Consulta as vendas do periodo
            sale.all(), # TESTAR
            Employee.nome.label("funcionario") # TESTAR
        ).filter(
            sale.cr == cr, # Filtro por CR
            sale.data >= init_date, # Data tem que ser maior ou igual a data inicial
            sale.data < end_date # Finaliza a data com o final do dia
        ).join( # Inner join com funcionarios
            Employee, Employee.matricula == sale.matricula 
        ).order_by(
            sale.data.desc()
        ).all()
        return [s.to_dict() for s in sales] # Retorna uma lista de vendas de acordo com a data selecionada

    @classmethod
    def _search_by_cr(sale, cr): # Retorna as vendas por cr
        return [s.to_dict() for s in sale.query.filter(sale.cr==cr).all()]