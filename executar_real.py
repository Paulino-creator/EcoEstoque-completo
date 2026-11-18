"""Serve o front-end junto da API real existente em app.py.

REQUER: app.py, banco.py, modelo.py, daos.py no mesmo diretorio;
MySQL/MariaDB funcionando e banco ecoestoque criado.
"""
from pathlib import Path
import pymysql
from flask import jsonify, send_from_directory

from app import app
from banco import obter_conexao

FRONTEND = Path(__file__).resolve().parent / "frontend"


@app.get("/painel")
def painel_dws():
    return send_from_directory(FRONTEND, "index.html")


@app.get("/frontend/<path:filename>")
def arquivos_dws(filename):
    return send_from_directory(FRONTEND, filename)


def consultar(sql):
    conexao = obter_conexao()
    try:
        with conexao.cursor() as cursor:
            cursor.execute(sql)
            return jsonify(cursor.fetchall())
    finally:
        conexao.close()


@app.get("/api/categorias")
def categorias_dws():
    try:
        return consultar("SELECT id_categoria, nome_categoria FROM CATEGORIA ORDER BY nome_categoria")
    except pymysql.MySQLError:
        return jsonify({"erro": "Não foi possível consultar categorias."}), 503


@app.get("/api/localizacoes")
def localizacoes_dws():
    try:
        return consultar("SELECT id_localizacao, CONCAT(bloco, ' • ', COALESCE(armario, '')) AS nome_localizacao FROM LOCALIZACAO ORDER BY bloco, armario")
    except pymysql.MySQLError:
        return jsonify({"erro": "Não foi possível consultar localizações."}), 503


@app.get("/api/itens-emprestimos")
def itens_emprestimos_dws():
    try:
        return consultar("SELECT id_item_emprestimo, id_emprestimo, id_material, quantidade_emprestada, status_emprestimo, estado_devolucao FROM ITEM_EMPRESTIMO ORDER BY id_item_emprestimo DESC")
    except pymysql.MySQLError:
        return jsonify({"erro": "Não foi possível consultar itens de empréstimos."}), 503


@app.get("/api/itens-reserva")
def itens_reserva_dws():
    try:
        return consultar("SELECT id_item_reserva, id_reserva, id_material, qtd_reserva FROM ITEM_RESERVA ORDER BY id_item_reserva DESC")
    except pymysql.MySQLError:
        return jsonify({"erro": "Não foi possível consultar itens de reservas."}), 503


if __name__ == "__main__":
    print("\nEcoEstoque - modo REAL (MySQL)")
    print("Abra: http://127.0.0.1:5001/painel\n")
    app.run(host="127.0.0.1", port=5001, debug=False)
