
import pymysql


CONFIG = {
    "host": "127.0.0.1",
    "port": 3306,
    "user": "root",
    "password": "",
    "charset": "utf8mb4",
    "cursorclass": pymysql.cursors.DictCursor
}


def criar_banco():
    conexao = pymysql.connect(**CONFIG, autocommit=True)

    try:
        with conexao.cursor() as cursor:
            cursor.execute("""
                CREATE DATABASE IF NOT EXISTS ecoestoque
                CHARACTER SET utf8mb4
                COLLATE utf8mb4_unicode_ci
            """)
    finally:
        conexao.close()


def obter_conexao():
    return pymysql.connect(
        **CONFIG,
        database="ecoestoque"
    )


if __name__ == "__main__":
    try:
        criar_banco()

        conexao = obter_conexao()

        try:
            with conexao.cursor() as cursor:
                cursor.execute("SELECT DATABASE() AS banco")
                resultado = cursor.fetchone()

                print("Conexão realizada com sucesso!")
                print("Banco:", resultado["banco"])
        finally:
            conexao.close()

    except pymysql.MySQLError as erro:
        print("Erro ao conectar ao MySQL:")
        print(erro)
