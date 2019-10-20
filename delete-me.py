import pymysql
import os
import subprocess
import io
import json
import logging
import os
import os.path
import re
import subprocess
import unittest
import pymysql


vini = 0
samuel = 1

samuel_cmd = "mysql -u root"




def cria_tudo():
    path = './sql'

    files = []
    for r, d, f in os.walk(path):
        for file in f:
            if '.sql' in file:
                files.append(os.path.join(r, file))

    for f in files:
        print(f)



    for f in files:

        with open(f, 'rb') as script:
            global config

            try:
                if(samuel):

                    subprocess.run(
                    [
                    samuel_cmd + script
                    ], 
                    stdin=f
                    )
                    print("roda aqui")
            except:
                pass

        
    


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


if __name__ == '__main__':
    global config
    with open('config_tests.json', 'r') as f:
        config = json.load(f)
    cria_tudo()
