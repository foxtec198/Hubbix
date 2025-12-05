from general.models.base_model import BaseModel

class Client(BaseModel):
    __bind_key__ = "analytics"
    __tablename__ = "clients"