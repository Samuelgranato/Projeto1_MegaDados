import io
import json
import logging
import os
import os.path
import re
import subprocess
import unittest
import pymysql

from projeto import *

class TestProjeto(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        global config
        cls.connection = pymysql.connect(
            host=config['HOST'],
            user=config['USER'],
            password=config['PASS'],
            database='projeto_dados'
        )

    @classmethod
    def tearDownClass(cls):
        cls.connection.close()

    def setUp(self):
        conn = self.__class__.connection
        with conn.cursor() as cursor:
            cursor.execute('START TRANSACTION')

    def tearDown(self):
        conn = self.__class__.connection
        with conn.cursor() as cursor:
            cursor.execute('ROLLBACK')

    def test_adiciona_usuario(self):
        conn = self.__class__.connection

        usuario1 = {
            'nome':'vinicius',
            'login': 'vinigl',
            'sobrenome':'lima',
            'email':'viniciusegl1@al.insper.edu.br',
            'cidade_idcidade':'1'
        }


        usuario2 = {
            'nome':'samuel',
            'login': 'samuelgranato',
            'sobrenome':'granwato',
            'email':'samuelvwgb@al.insper.edu.br',
            'cidade_idcidade':'1'
        }



        adiciona_usuario(conn, usuario1)
        adiciona_usuario(conn, usuario2)


        try:
            adiciona_usuario(conn, usuario1)
            self.fail("Mesmo usuário 2 vezes!")
        except ValueError as e:
            pass

        id1 = acha_usuario_login(conn, usuario1['login'])
        id2 = acha_usuario_login(conn, usuario1['login'])


        self.assertIsNotNone(id1)
        self.assertIsNotNone(id2)


    def test_add_post(self):
        conn = self.__class__.connection

        usuario1 = {
            'nome':'vinicius2',
            'login': 'vinigl2',
            'sobrenome':'lima',
            'email':'viniciu2sgl1@al.insper.edu.br',
            'cidade_idcidade':'1'
        }

        adiciona_usuario(conn, usuario1)
        id1 = acha_usuario_login(conn, usuario1['login'])


        post = {
            'user_iduser_p':id1,
            'titulo':'test',
            'texto':'texto @vinigl @dwd #pica-pau',
            'url':'abc.com'
        }

        adiciona_post(conn,post)

        idpost = acha_post_bypost(conn,post)
        self.assertIsNotNone(idpost)


    def test_update_post(self):
        conn = self.__class__.connection

        usuario1 = {
            'nome':'vinicius2',
            'login': 'vinigl2',
            'sobrenome':'lima',
            'email':'viniciu2sgl1@al.insper.edu.br',
            'cidade_idcidade':'1'
        }

        adiciona_usuario(conn, usuario1)
        id1 = acha_usuario_login(conn, usuario1['login'])


        post = {
            'user_iduser_p':id1,
            'titulo':'antes',
            'texto':'texto @vinigl @dwd #pica-pau',
            'url':'abc.com'
        }

        adiciona_post(conn,post)

        idpost = acha_post_bypost(conn,post)


        post = {
            'user_iduser_p':id1,
            'titulo':'mudado',
            'texto':'texto @vinigl @dwd #pica-pau',
            'url':'abc.com'
        }

        update_post(conn,idpost,post)

        self.assertEqual(visualiza_texto_post(conn,idpost),post['texto'])
        self.assertEqual(visualiza_url_post(conn,idpost),post['url'])
        self.assertEqual(visualiza_titulo_post(conn,idpost),post['titulo'])
        

    def test_delete_post(self):
        conn = self.__class__.connection

        usuario1 = {
            'nome':'vinicius2',
            'login': 'vinigl2',
            'sobrenome':'lima',
            'email':'viniciu2sgl1@al.insper.edu.br',
            'cidade_idcidade':'1'
        }

        adiciona_usuario(conn, usuario1)
        id1 = acha_usuario_login(conn, usuario1['login'])


        post = {
            'user_iduser_p':id1,
            'titulo':'antes',
            'texto':'texto @vinigl @dwd #pica-pau',
            'url':'abc.com'
        }

        adiciona_post(conn,post)

        idpost = acha_post_bypost(conn,post)
        apaga_post(conn,idpost)

        self.assertEqual(get_post_status(conn,idpost),0)


    def test_ativa_post(self):
        conn = self.__class__.connection

        usuario1 = {
            'nome':'vinicius2',
            'login': 'vinigl2',
            'sobrenome':'lima',
            'email':'viniciu2sgl1@al.insper.edu.br',
            'cidade_idcidade':'1'
        }

        adiciona_usuario(conn, usuario1)
        id1 = acha_usuario_login(conn, usuario1['login'])


        post = {
            'user_iduser_p':id1,
            'titulo':'antes',
            'texto':'texto @vinigl @dwd #pica-pau',
            'url':'abc.com'
        }

        adiciona_post(conn,post)

        idpost = acha_post_bypost(conn,post)
        ativa_post(conn,idpost)

        self.assertEqual(get_post_status(conn,idpost),1)

        
    def test_adiciona_passaro(self):
        conn = self.__class__.connection

        passaro = {
            'especie':'calopsita',
        }

        adiciona_passaro(conn, passaro)

        id = acha_passaro(conn, passaro)
        self.assertIsNotNone(id)

  
    def test_lista_passaro(self):
        conn = self.__class__.connection

        passaro1 = {
            'especie':'calopsita',
        }
        passaro2 = {
            'especie':'piriquito',
        }
        passaro3 = {
            'especie':'pomba?',
        }

        adiciona_passaro(conn, passaro1)
        adiciona_passaro(conn, passaro2)
        adiciona_passaro(conn, passaro3)

        lista_pass = lista_passaros(conn)

        self.assertEqual(lista_pass[0][1],passaro1['especie'])
        self.assertEqual(lista_pass[1][1],passaro2['especie'])
        self.assertEqual(lista_pass[2][1],passaro3['especie'])

    def test_like(self):
        conn = self.__class__.connection

        usuario1 = {
            'nome':'vinicius2',
            'login': 'vinigl2',
            'sobrenome':'lima',
            'email':'viniciu2sgl1@al.insper.edu.br',
            'cidade_idcidade':'1'
        }

        adiciona_usuario(conn, usuario1)
        id1 = acha_usuario_login(conn, usuario1['login'])


        post = {
            'user_iduser_p':id1,
            'titulo':'antes',
            'texto':'texto @vinigl @dwd #pica-pau',
            'url':'abc.com'
        }

        adiciona_post(conn,post)
        idpost = acha_post_bypost(conn,post)

        self.assertEqual(get_curtir(conn,idpost),0)


        id_usuario = acha_usuario_login(conn, usuario1['login'])

        # print(idpost)
        curtida = {
            'iduser': id_usuario,
            'idpost': idpost,
            'valor' : 1
        }

        update_curtir(conn,curtida)        
        self.assertEqual(get_curtir(conn,idpost),1)
        update_curtir(conn,curtida)        
        self.assertEqual(get_curtir(conn,idpost),0)


        curtida = {
            'iduser': id_usuario,
            'idpost': idpost,
            'valor' : -1
        }


        update_curtir(conn,curtida)        
        self.assertEqual(get_curtir(conn,idpost),-1)
        update_curtir(conn,curtida)        
        self.assertEqual(get_curtir(conn,idpost),0)



    def test_list_url_passaro(self):
        conn = self.__class__.connection


        passaro1 = {
            'especie' : 'pica-pau'
        }
        
        passaro2 = {
            'especie' : 'periquito'
        }

        
        adiciona_passaro(conn,passaro1)
        adiciona_passaro(conn,passaro2)


        usuario1 = {
            'nome':'vinicius2',
            'login': 'vinigl2',
            'sobrenome':'lima',
            'email':'viniciu2sgl1@al.insper.edu.br',
            'cidade_idcidade':'1'
        }

        adiciona_usuario(conn, usuario1)
        id1 = acha_usuario_login(conn, usuario1['login'])


        post1 = {
            'user_iduser_p':id1,
            'titulo':'antes',
            'texto':'texto @vinigl @dwd #pica-pau',
            'url':'abc.com'
        }

        usuario2 = {
            'nome':'samuel',
            'login': 'samuelvgb',
            'sobrenome':'lima',
            'email':'samuel@al.insper.edu.br',
            'cidade_idcidade':'1'
        }

        adiciona_usuario(conn, usuario2)
        id2 = acha_usuario_login(conn, usuario2['login'])


        post2 = {
            'user_iduser_p':id2,
            'titulo':'antes',
            'texto':'texto @vinigl @dwd #periquito',
            'url':'def.com'
        }


        adiciona_post(conn,post1)
        adiciona_post(conn,post2)


        result = list_URL_passaros(conn)

        expected = [('abc.com','pica-pau'),('def.com','periquito')]

        self.assertEqual(result,expected)



    def test_list_received_mencao(self):
        conn = self.__class__.connection


        usuario1 = {
                'nome':'vinicius2',
                'login': 'vinigl',
                'sobrenome':'lima',
                'email':'viniciu2sgl1@al.insper.edu.br',
                'cidade_idcidade':'1'
            }

        adiciona_usuario(conn, usuario1)
        id1 = acha_usuario_login(conn, usuario1['login'])


        post1 = {
            'user_iduser_p':id1,
            'titulo':'antes',
            'texto':'texto @famoso @dwd #pica-pau',
            'url':'abc.com'
        }

        usuario2 = {
            'nome':'samuel',
            'login': 'samuelvgb',
            'sobrenome':'lima',
            'email':'samuel@al.insper.edu.br',
            'cidade_idcidade':'1'
        }

        adiciona_usuario(conn, usuario2)
        id2 = acha_usuario_login(conn, usuario2['login'])


        post2 = {
            'user_iduser_p':id2,
            'titulo':'antes',
            'texto':'texto @famoso @dwd #periquito',
            'url':'def.com'
        }

        usuario3 = {
            'nome':'famoso',
            'login': 'famoso',
            'sobrenome':'lima',
            'email':'famoso@al.insper.edu.br',
            'cidade_idcidade':'1'
        }
        adiciona_usuario(conn, usuario3)

        adiciona_post(conn,post1)
        adiciona_post(conn,post2)



        expected = ['vinigl', 'samuelvgb']
        received = list_received_mencao(conn,usuario3['login'])
        self.assertEqual(received,expected)




def run_sql_script(filename):
    global config
    with open('./sql/' + filename, 'rb') as f:
        subprocess.run(
            [
                config['MYSQL'], 
                '-u', config['USER'], 
                '-p' + config['PASS'], 
                '-h', config['HOST']
            ], 
            stdin=f
        )

def setUpModule():
    filenames = [entry for entry in os.listdir('./sql') ]
    for filename in filenames:
        run_sql_script(filename)

def tearDownModule():
    run_sql_script('../tear_down.sql')

if __name__ == '__main__':
    global config
    with open('config_tests_samuel.json', 'r') as f:
        config = json.load(f)
    logging.basicConfig(filename=config['LOGFILE'], level=logging.DEBUG)
    unittest.main(verbosity=2)
