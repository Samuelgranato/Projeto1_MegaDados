import pymysql
import json

with open('../config_tests.json', 'r') as f:
        config = json.load(f)

connection = pymysql.connect(
            host=config['HOST'],
            user=config['USER'],
            password=config['PASS'],
            database='projeto_dados',
            autocommit=True
        )
    