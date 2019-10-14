import pymysql


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


