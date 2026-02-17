import sqlite3

def conectar(query, params=()):
    conexao = sqlite3.connect("db/sql/mixcamp.db")
    cursor = conexao.cursor()

    cursor.execute(query, params)
    response = cursor.fetchall()
    conexao.commit()
    
    desconectar(conexao,cursor)
    return response





def desconectar(conexao,cursor):
    cursor.close()
    conexao.close()