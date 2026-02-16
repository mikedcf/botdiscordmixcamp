import sqlite3

def conectar(query):
    conexao = sqlite3.connect("mixcamp.db")
    cursor = conexao.cursor()

    cursor.execute(query)
    response = cursor.fetchall()
    conexao.commit()
    
    desconectar(conexao,cursor)
    return response





def desconectar(conexao,cursor):
    cursor.close()
    conexao.close()