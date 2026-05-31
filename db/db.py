import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()


def conectar(query, params=None, fetch=False):
    conexao = None
    cursor = None

    try:
        conexao = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_DATABASE')
        )

        cursor = conexao.cursor(
            dictionary=True,
            buffered=True
        )

        cursor.execute(query, params or ())

        response = None

        if fetch:
            response = cursor.fetchall()

        conexao.commit()

        return response

    except Exception as e:
        print(f"Erro banco: {e}")
        return None

    finally:
        if cursor:
            cursor.close()

        if conexao and conexao.is_connected():
            conexao.close()