from fastapi import FastAPI, HTTPException
import logging
import pymysql
from starlette.requests import Request
import os
import datetime

from connection import *
os.chdir('../')
from projeto import *
os.chdir('api/')

from models import *


app = FastAPI()


@app.get("/")
def read_root(req : Request):
    
    #     raise HTTPException(status_code=404, detail="Erro na operacao")
    infos = vars(req.headers)['_list']
   
    request_infos = {}
    for i in infos:
        key = i[0].decode('ASCII')
        value = i[1].decode('ASCII')

        request_infos[key] = value

    OS = request_infos['user-agent'].split(" ")[2]
    
    useful_info = {'host': request_infos['host'], 
                   'browser': request_infos['user-agent'], 
                   'OS' : OS, 
                   'criado_ts': datetime.datetime.now()}
    
    return useful_info


@app.get("/usuario")  # Procura usuario por nome e sobrenomes
def acha_usuario(usuario: Usuario):
    result = acha_usuario_nome(connection, usuario.nome, usuario.sobrenome)
    return result


@app.post("/usuario")  # Insere usuario
def cria_usuario(usuario: Usuario):
    cursor = connection.cursor()
    nome_cidade = usuario.cidade.capitalize()
    id_cidade = get_nome_cidade(connection, nome_cidade)

    usuario_add = {
        'nome': usuario.nome,
        'sobrenome': usuario.sobrenome,
        'email': usuario.email,
        'cidade_idcidade': id_cidade,
        'login': usuario.login
    }

    adiciona_usuario(connection, usuario_add)
    return "Sucesso"


@app.get("/posts")
def acha_posts(post: Post_Acha, req: Request):
    post_find = {
        'user_iduser': post.iduser,
        'titulo': post.titulo
    }
    resultado = acha_post(connection, post_find)

    infos = vars(req.headers)['_list']
   
    request_infos = {}
    for i in infos:
        key = i[0].decode('ASCII')
        value = i[1].decode('ASCII')

        request_infos[key] = value
    
    OS = request_infos['user-agent'].split(" ")[2]
    
    useful_info = {'host': request_infos['host'], 
                   'browser': request_infos['user-agent'], 
                   'OS' : OS, 
                   'criado_ts': datetime.datetime.now()}
    
    gera_log(useful_info)

    return resultado


@app.post("/posts")
def cria_post(post: Post_Cria):
    post_cria = {
        'id': post.iduser,
        'titulo': post.titulo,
        'texto': post.texto,
        'url': post.url
    }

    adiciona_post(connection, post_cria)

@app.put("/posts")
def atualiza_post(post: Post_Atualiza):
    pass

@app.delete("/posts")
def deleta_post(post: Post_Apaga):
    apaga_post(connection, post.id)
    return "Post deletado com sucesso"

@app.get("lista_posts")
def todos_posts():
    posts = lista_posts(connection)

    return posts

@app.get("/passaros")
def acha_passaros():

    passaros = lista_passaros(connection)

    return passaros

@app.post("/passaros")
def cria_passaro(passaro: Passaro):
    adiciona_passaro(connection, passaro.especie)