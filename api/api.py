from fastapi import FastAPI
from pydantic import BaseModel
import logging
import pymysql

#  LOGGING CONFIGS
logger = logging.getLogger('API')
logger.setLevel(logging.DEBUG) #On console

ch = logging.FileHandler("/home/vinicius/Documents/1help/repos/logs/access.log")
ch.setLevel(logging.INFO) #On file


formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

ch.setFormatter(formatter)
logger.addHandler(ch)

#Logging levels
#CRITICAL
#ERROR
#WARNING
#INFO
#DEBUG
#NOTSET

# from connection import *

class Usuario(BaseModel):
    nome: str
    sobrenome: str
    email: str

app = FastAPI()


@app.get("/")
def read_root():
    logger.info('bateu aqui')
    return {"Hello": "World"}

@app.get("/a")
def a():
    logger.info('OBA')
    return {"Hello": "World"}


@app.post("/db")
def acha_usuario(usuario : Usuario):
    cursor = connection.cursor()
    q = 'SELECT id, nome, sobrenome FROM user WHERE nome = %s AND sobrenome = %s;'
    cursor.execute(q, (usuario.nome, usuario.sobrenome))
    cursor.close()
    return cursor.fetchall()

    
