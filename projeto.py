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

    files.sort()
    print(files)

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
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO user (login, nome, sobrenome, email, cidade_idcidade) VALUES (%s, %s, %s, %s, %s)', (usuario['login'],usuario['nome'], usuario['sobrenome'], usuario['email'], usuario['cidade_idcidade']))
    except pymysql.err.IntegrityError as e:
        raise ValueError(f'Não posso inserir {usuario["nome"]} na tabela user')

def acha_usuario_login(conn, login):
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM user WHERE login = %s ', (login))
        res = cursor.fetchone()
        if res:
            return res[0]
        else:
            return None

def acha_usuario_id(conn, id):
    with conn.cursor() as cursor:
        cursor.execute('SELECT * FROM user WHERE iduser = %s ', (id))
        res = cursor.fetchone()
        if res:
            return res[1]
        else:
            return None

def acha_usuario_nome(conn, nome, sobrenome):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user WHERE nome = %s AND sobrenome = %s', (nome, sobrenome))
    res = cursor.fetchone()
    if res:
        return res
    else:
        return None

def adiciona_cidade(connection,nome):
    cur = connection.cursor()
    cur.execute("INSERT INTO cidade (nome) VALUES (%s)",(nome))

def get_nome_cidade(connection,nome_cidade):
    cur = connection.cursor()
    cur.execute("SELECT id FROM cidade WHERE idcidade = %s",(nome_cidade))

    c = cur.fetchall()

    for i in c:
        return i[1]
    

def adiciona_post(connection,post):
    cur = connection.cursor()
    cur.execute("INSERT INTO post (user_iduser_p,titulo,texto,url) VALUES (%s,%s,%s,%s)",(post['user_iduser_p'],post['titulo'],post['texto'],post['url']))
     
    
    post_id = acha_post_bypost(connection,post)
    
    
    
    texto = post["texto"]
    for palavra in texto.split(" "):
        if("@" in palavra):
            user_mencionado = palavra.split("@")[1]
            
            user_mencionado_id = acha_usuario_login(connection,user_mencionado)

            if(user_mencionado_id != None):
                try:

                    cur.execute("INSERT INTO post_menciona_user (post_idpost_mu,user_iduser_mu) VALUES (%s,%s)",(post_id,user_mencionado_id))

                except pymysql.err.IntegrityError as e:
                    raise ValueError(f'Não posso inserir {user_mencionado} na tabela user')
                
            
        
        if("#" in palavra):
            passaro_mencionado = palavra.split("#")[1]

            passaro = {
                'especie':passaro_mencionado
            }  
            
            passaro_mencionado_id = acha_passaro(connection,passaro)
            
    
            
            if(passaro_mencionado_id != None):
                try:
                    cur.execute("INSERT INTO post_menciona_passaro (post_idpost_mp,passaro_idpassaro_mp) VALUES (%s,%s)",(post_id,passaro_mencionado_id))
                except pymysql.err.IntegrityError as e:
                    raise ValueError(f'Não posso inserir {passaro_mencionado} na tabela post_menciona_passaro')
                    
                    
    curtida = {
    'iduser':post['user_iduser_p'],
    'idpost':post_id
    }
             
    cria_curtir(connection,curtida)



def apaga_post(connection,idpost):
    cur = connection.cursor()
    cur.execute("UPDATE post SET is_active=0 WHERE idpost = %s",(idpost))
 
def ativa_post(connection,idpost):
    cur = connection.cursor()
    cur.execute("UPDATE post SET is_active=1 WHERE idpost = %s",(idpost))


def lista_usuarios(conn):
    cur = conn.cursor()
    cursor.execute('SELECT id from user')
    res = cursor.fetchall()
    users = tuple(x[0] for x in res)
    return users

def gera_log(connection,log):
    cur = connection.cursor()
    cur.execute("INSERT INTO log (user_iduser_l,os,browser,ip,criado_ts) VALUES (%s,%s,%s,%s,%s)",(log["user_iduser_l"],log["os"],log["browser"],log["ip"],log["criado_ts"])) 



def adiciona_passaro(conn, passaro):
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO passaro (especie) VALUES (%s)', (passaro['especie']))
    except pymysql.err.IntegrityError as e:
        raise ValueError(f'Não posso inserir {especie} na tabela user')



def acha_passaro(conn, passaro):
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM passaro WHERE especie = %s ', (passaro['especie']))
    res = cursor.fetchone()
    if res:
        return res[0]
    else:
        return None

def acha_post(connection, post_titulo):
    cur = connection.cursor()
    cur.execute("SELECT * FROM post WHERE titulo = %s",(post_titulo))
     
    c = cur.fetchall()
    for i in c:
        return i[0]

def acha_post_bypost(connection,post):
    cur = connection.cursor()
    cur.execute("SELECT * FROM post WHERE user_iduser_p = %s AND titulo = %s",(post['user_iduser_p'],post['titulo']))
     
    c = cur.fetchall()

    for i in c:
        return i[0]
                         
def acha_post_id(connection,idpost):
    cur = connection.cursor()
    cur.execute("SELECT * FROM post WHERE idpost = %s ",(idpost))
     
    c = cur.fetchall()

    for i in c:
        return i[0]


def lista_posts(connection):
    cur = connection.cursor()
    cur.execute("SELECT * FROM post")
     
    c = cur.fetchall()

    return c

def lista_posts_desc(connection):
    cur = connection.cursor()
    cur.execute("SELECT * FROM post WHERE is_active=1 ORDER BY idpost DESC")
     
    c = cur.fetchall()

    return c

def lista_passaros(connection):
    cur = connection.cursor()
    cur.execute("SELECT * FROM passaro")

    c = cur.fetchall()

    return c


def update_post(connection,idpost,post):
    cur = connection.cursor()
    cur.execute("UPDATE post SET titulo = %s, texto = %s, url = %s WHERE idpost = %s",(post["titulo"],post["texto"],post["url"],idpost))

def acha_passaro(connection, passaro):
    cur = connection.cursor()
    cur.execute('SELECT * FROM passaro WHERE especie = %s ', (passaro['especie']))
    res = cur.fetchone()
    if res:
        return res[0]
    else:
        return None

def visualiza_texto_post(connection,idpost):
    cur = connection.cursor()
    cur.execute("SELECT * FROM post where idpost = %s",(idpost))

    c = cur.fetchall()

    for i in c:
        return i[3]

def visualiza_url_post(connection,idpost):
    cur = connection.cursor()
    cur.execute("SELECT * FROM post where idpost = %s",(idpost))

    c = cur.fetchall()

    for i in c:
        return i[4]

def visualiza_titulo_post(connection,idpost):
    cur = connection.cursor()
    cur.execute("SELECT * FROM post where idpost = %s",(idpost))

    c = cur.fetchall()

    for i in c:
        return i[2]


def get_post_status(connection,idpost):
    cur = connection.cursor()
    cur.execute("SELECT * FROM post where idpost = %s",(idpost))

    c = cur.fetchall()

    for i in c:
        return i[5]

def atualiza_preferencia(connection, preferencia, usuario_id, passaro_id):
    cur = connection.cursor()
    cur.execute("UPDATE user_has_passaro SET gosta = %s WHERE user_iduser_hp = %s AND passaro_idpassado_hp = %s", (preferencia, usuario_id, passaro_id))
    cur.close()
    
def os_popular(connection):
    cur = connection.cursor()
    cur.execute("SELECT os, count(os) as total FROM log GROUP BY os")
    resultado = cur.fetchall()
    cur.close()

    return resultado

def tabela_cruzado(connection):
    cursor = connection.cursor()
    q = '''SELECT 
               os, browser, COUNT(os) as total
            FROM 
                log
            GROUP BY 
                os,
                browser
            '''
    cursor.execute(q)
    r = cursor.fetchall()
    cursor.close()
    return r
    


def cria_curtir(connection,curtida):
    cur = connection.cursor()
    cur.execute("INSERT INTO post_likes (idpost,iduser) VALUES (%s,%s)",(curtida["idpost"],curtida["iduser"]))
 
def update_curtir(connection,curtida):
    cur = connection.cursor()
    cur.execute("UPDATE post_likes set curtida = %s WHERE idpost = %s AND iduser = %s",(curtida["valor"],curtida["idpost"],curtida["iduser"]))

def get_curtir(connection,idpost):

    cur = connection.cursor()
    cur.execute("SELECT * from post_likes")
    
    c = cur.fetchall()

    for i in c:
        return i[2]


def acha_post_id_ret_user(connection,idpost):
    cur = connection.cursor()
    cur.execute("SELECT * FROM post WHERE idpost = %s ",(idpost))
     
    c = cur.fetchall()

    for i in c:
        return i[1]


def list_received_mencao(connection,login):
    cur = connection.cursor()

    id_usuario = acha_usuario_login(connection,login)

    
    cur.execute("SELECT * from post_menciona_user WHERE user_iduser_mu = %s",(id_usuario))
    resultado = cur.fetchall()
    cur.close()
    
    usuarios = []
    
    for mencao in resultado:
        id_usuario_mencionou = acha_post_id_ret_user(connection,mencao[0])
        if id_usuario_mencionou not in usuarios:
            usuarios.append(id_usuario_mencionou)
    
    usuarios_login = []
    for usuario in usuarios:
        usuarios_login.append(acha_usuario_id(connection,usuario))
        

    return usuarios_login

def list_URL_passaros(connection):
    cur = connection.cursor()
    cur.execute("SELECT * from post_menciona_passaro")
    
    c = cur.fetchall()

    
    return_values = []
    for i in c:


        return_values.append((acha_post_id_ret_url(connection,i[0]),acha_passaro_id(connection,i[1])))

    return return_values


def acha_post_id_ret_url(connection,idpost):
    cur = connection.cursor()
    cur.execute("SELECT * FROM post WHERE idpost = %s ",(idpost))
     
    c = cur.fetchall()

    for i in c:
        return i[4]
    
    
def acha_passaro_id(connection, id):
    cur = connection.cursor()
    cur.execute('SELECT * FROM passaro WHERE idpassaro = %s ', (id))
    res = cur.fetchone()
    if res:
        return res[1]
    else:
        return None


def usuario_popular(connection):
    cursor = connection.cursor()
    q = '''SELECT 
                cidade.idcidade, COUNT(post.idpost) as total
            FROM 
                user, post, post_menciona_user, cidade
            WHERE 
                post_menciona_user.post_idpost_mu=user.iduser 
                AND post_menciona_post_mu=post.idpost
                AND post_menciona_post_mu=is_active=1
            GROUP BY 
                cidade.idcidade
                MAX(total)
            
            '''
    cursor.execute(q)
    cursor.close()

def likes(connection, like):
    cursor = connection.cursor()
    q = '''UPDATE 
                post_likes
            SET 
                curtida=%s
            WHERE
                idpost=%s 
                AND iduser=%s
            
            '''
    cursor.execute(q, (like.like, like.idpost, like.iduser))
    cursor.close()

