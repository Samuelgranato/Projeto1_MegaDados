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

        usuario = {
            'nome':'vinicius',
            'sobrenome':'lima',
            'email':'viniciusgl1@al.insper.edu.br',
            'cidade_idcidade':'1'
        }

        adiciona_usuario(conn, usuario)

        id = acha_usuario(conn, usuario)
        self.assertIsNotNone(id)


    def test_adiciona_passaro(self):
        conn = self.__class__.connection

        passaro = {
            'especie':'calopsita',
        }

        adiciona_passaro(conn, passaro)
        


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
    with open('config_tests.json', 'r') as f:
        config = json.load(f)
    logging.basicConfig(filename=config['LOGFILE'], level=logging.DEBUG)
    unittest.main(verbosity=2)
