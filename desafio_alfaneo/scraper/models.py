from pydantic import BaseModel

valid_ufs = ['AC', 'AL', 'AP','AM','BA','CE','DF','ES','GO','MA','MT','MS','MG','PA','PB','PR','PE','PI','RJ','RN','RS','RO','RR','SC','SP','SE','TO']

class Request(BaseModel):
    name: str
    uf: str

class Response(BaseModel):
    oab: str
    nome: str
    uf: str
    categoria: str
    situacao: str