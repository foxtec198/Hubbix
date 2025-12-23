from general.models.base_model import BaseModel, db

class Employee(BaseModel):
    __bind_key__ = "manager" # Define qual BD vamos utilizar
    __tablename__ = "funcionarios" # Define o nome da tabela do BD
    __table_args__ = {'extend_existing': True}  # <- evita erro se já existir
    
    matricula = db.Column(db.Integer(), primary_key=True)
    nome = db.Column(db.String(50), nullable=False)
    permissao = db.Column(db.String(), nullable=False)
    hash = db.Column(db.String(128), nullable=False)
    photo = db.Column(db.String)
    cr = db.Column(db.String(100), nullable=False)
    grupodecliente = db.Column(db.String(100), nullable=False)

    @classmethod
    def _search_by_cr(cls, cr): 
        res = cls.query.filter_by(cr=cr).all()
        employees = []
        for employee in res:
            employees.append({
                "nome": employee.nome,
                "matricula": employee.matricula,
                "perm": employee.permissao,
                "img": employee.photo
            })
        return employees

    @classmethod
    def _search_by_mat(cls, mat, cr):
        return cls.query.filter_by(matricula=mat, cr=cr).first()


        
        

        