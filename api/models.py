
from pydantic import BaseModel

class Teste(BaseModel):
    a: str

class Acha_Usuario(BaseModel):
    nome: str
    sobrenome: str
    

class Adiciona_Usuario(BaseModel):
    nome: str
    sobrenome: str
    email: str
    login: str
    cidade: int


class Post_Acha(BaseModel):
    titulo: str


class Post_Cria(BaseModel):
    iduser: int
    titulo: str
    url: str
    texto: str
    mencao_usuario: str
    mencao_passaro: str

class Post_Apaga(BaseModel):
    id: int

class Post_Atualiza(BaseModel):
    pass

class Passaro(BaseModel):
    especie: str

class Preferencia(BaseModel):
    gosta: int
    userid: int
    passaroid: int

class Likes(BaseModel):
    like: int
    idpost: int
    iduser: int