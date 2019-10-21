from fastapi import FastAPI, HTTPException
import logging
import pymysql
from starlette.requests import Request
import os
import datetime

from connection import *
os.chdir('../')
from projeto import *
os.chdir('./api')

from models import *


app = FastAPI()


@app.post("/")
def read_root(teste: Teste):
    
    return 


@app.get("/usuario")  # Procura usuario por nome e sobrenomes
def acha_usuario(usuario: Acha_Usuario):
    result = acha_usuario_nome(connection, usuario.nome, usuario.sobrenome)
    return result


@app.post("/usuario")  # Insere usuario
def cria_usuario(usuario: Adiciona_Usuario):
    # nome_cidade = usuario.cidade.capitalize()
    # id_cidade = get_nome_cidade(connection, nome_cidade)

    usuario_add = {
        'nome': usuario.nome,
        'sobrenome': usuario.sobrenome,
        'email': usuario.email,
        'cidade_idcidade': usuario.idcidade,
        'login': usuario.login
    }

    adiciona_usuario(connection, usuario_add)
    return "Sucesso"

@app.post("/preferencia")
def cria_preferencia(preferencia: Preferencia):
    
    atualiza_preferencia(connection, 
                         preferencia.gosta,
                         preferencia.userid,
                         preferencia.passaroid)


@app.get("/posts/{idpost}")
def acha_posts(req: Request, idpost:int):
    # post_find = {
    #     'titulo': post.titulo
    # }
    print(idpost)
    resultado = acha_post(connection, idpost)

    infos = vars(req.headers)['_list']
   
    request_infos = {}
    for i in infos:
        key = i[0].decode('ASCII')
        value = i[1].decode('ASCII')

        request_infos[key] = value
    
    print(request_infos['user-agent'].split(" "))
    try:
        OS = request_infos['user-agent'].split(" ")[2]
    except:
        OS = request_infos['user-agent'].split(" ")[0]

    print(len(request_infos['user-agent']))
    useful_info = {'user_iduser_l':1,
                   'ip': request_infos['host'], 
                   'browser': request_infos['user-agent'], 
                   'os' : OS, 
                   'criado_ts': datetime.datetime.now()}
    
    gera_log(connection, useful_info)

    return resultado

@app.get("/os_popular")
def lista_os():
    resultado = os_popular(connection)
    return resultado

@app.post("/posts")
def cria_post(post: Post_Cria):
    post_cria = {
        'user_iduser_p': post.iduser,
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

@app.get("/all_posts")
def todos_posts():
    posts = lista_posts(connection)

    return posts

@app.get("/posts_desc")
def todos_posts_desc():
    posts = lista_posts_desc(connection)

    return posts

@app.get("/passaros")
def procura_passaros():

    passaros = lista_passaros(connection)

    return passaros

@app.post("/passaros")
def cria_passaro(passaro: Passaro):
    adiciona_passaro(connection, passaro.especie)

@app.put("/likes")
def like_post(like : Likes):
    likes(connection, like)

@app.get("/tabela_cruzado")
def tabela_cruzada():
    return tabela_cruzado(connection)

@app.get("/mencao/{login}")
def lista_mencao(login: str):
    res = list_received_mencao(connection, login)

    return res 
    
@app.get("/url_passaro")
def url_passaro():
    res = list_URL_passaros(connection)
    
    return res