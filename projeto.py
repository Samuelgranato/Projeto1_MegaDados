import pymysql
import io
import json
import logging
import os
import os.path
import re
import subprocess
import unittest


def cria_tudo():
    global config

    # print("WARNING: Usando config vini")
    # with open('config_tests.json', 'r') as f:
    #     config = json.load(f)

    print("WARNING: Usando config samuel")
    with open('config_tests_samuel.json', 'r') as f:
        config = json.load(f)


    logging.basicConfig(filename=config['LOGFILE'], level=logging.DEBUG)



    path = './sql'
    files = []
    for r, d, f in os.walk(path):
        for file in f:
            if '.sql' in file:
                files.append(os.path.join(r, file)) 

    for f in files:
        print(f)
        with open(f, 'rb') as script:
             subprocess.run(
            [
                config['MYSQL'], 
                '-u', config['USER'], 
                '-p' + config['PASS'], 
                '-h', config['HOST']
            ], 
            stdin=script
        )


def adiciona_usuario(conn, usuario):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO user (nome, sobrenome, email, cidade_idcidade) VALUES (%s, %s, %s, %s)', (usuario['nome'], usuario['sobrenome'], usuario['email'], usuario['cidade_idcidade']))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso inserir {usuario["nome"]} na tabela user')

def acha_usuario(conn, nome, sobrenome):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id FROM perigo WHERE nome = %s AND sobrenome = %s', (nome, sobrenome))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

def adiciona_cidade(connection,nome):
    cur = connection.cursor()
    cur.execute("INSERT INTO cidade (nome) VALUES (%s)",(nome))

def acha_cidade(connection,idcidade):
    cur = connection.cursor()
    cur.execute("SELECT * FROM cidade WHERE idcidade = %s",('0'))

    c = cur.fetchall()

    for i in c:
        return i[0]


def adiciona_post(connection,post):
    cur = connection.cursor()
    cur.execute("INSERT INTO post (user_iduser_p,titulo,texto,url) VALUES (%s,%s,%s,%s)",(post['id'],post['titulo'],post['texto'],post['url']))
 

def apaga_post(connection,idpost):
    cur = connection.cursor()
    cur.execute("UPDATE post SET is_active=0 WHERE idpost = %s",(idpost))
 
def ativa_post(connection,idpost):
    cur = connection.cursor()
    cur.execute("UPDATE post SET is_active=1 WHERE idpost = %s",(idpost))



def lista_usuarios(conn):
    with conn.cursor() as cursor:
        cursor.execute('SELECT id from user')
        res = cursor.fetchall()
        perigos = tuple(x[0] for x in res)
        return perigos
    

def adiciona_passaro(conn, passaro):
    with conn.cursor() as cursor:
        try:
            cursor.execute('INSERT INTO passaro (especie) VALUES (%s)', (passaro['especie']))
        except pymysql.err.IntegrityError as e:
            raise ValueError(f'Não posso inserir {passaro["especie"]} na tabela user')



def get_cidade(conn,idcidade):
    with conn.cursor() as cursor:
        cursor.execute('SELECT idcidade FROM cidade WHERE nome = %s AND sobrenome = %s', (nome, sobrenome))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None


