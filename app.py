from datetime import date
from flask import Flask, jsonify, request
import pymysql

from modelo import Usuario, Material, Reserva, Emprestimo
from daos import UsuarioDAO, MaterialDAO, ReservaDAO, EmprestimoDAO

app = Flask(__name__)


@app.route("/")
def inicio():
    return jsonify({
        "projeto": "EcoEstoque",
        "mensagem": "Servidor Flask funcionando!"
    })


@app.route("/api/status")
def status():
    return jsonify({
        "sistema": "EcoEstoque",
        "servidor": "online",
        "banco": "nao verificado"
    })


# ROTAS DE USUÁRIOS

@app.route("/api/usuarios", methods=["GET", "POST"])
def usuarios():

    if request.method == "GET":
        try:
            lista = UsuarioDAO.listar_todos()
            return jsonify([u.para_dict() for u in lista])

        except pymysql.MySQLError:
            return jsonify({
                "erro": "Nao foi possivel consultar o banco."
            }), 503

    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({"erro": "Envie um JSON valido."}), 400

    nome = str(dados.get("nome_usuario") or "").strip()
    tipo = str(dados.get("tipo_usuario") or "").strip().lower()

    if not nome or tipo not in ("aluno", "professor", "admin"):
        return jsonify({
            "erro": "Informe nome e tipo de usuario validos."
        }), 400

    usuario = Usuario(
        nome_usuario=nome,
        tipo_usuario=tipo,
        email=str(dados.get("email") or "").strip(),
        matricula=str(dados.get("matricula") or "").strip(),
        cpf=str(dados.get("cpf") or "").strip()
    )

    try:
        UsuarioDAO.cadastrar(usuario)

    except pymysql.IntegrityError:
        return jsonify({
            "erro": "Dados duplicados ou invalidos para o banco."
        }), 409

    except pymysql.MySQLError:
        return jsonify({
            "erro": "Nao foi possivel cadastrar no banco."
        }), 503

    return jsonify(usuario.para_dict()), 201


# ROTAS DE MATERIAIS

@app.route("/api/materiais", methods=["GET", "POST"])
def materiais():

    if request.method == "GET":
        try:
            lista = MaterialDAO.listar_todos()
            return jsonify([m.para_dict() for m in lista])

        except pymysql.MySQLError:
            return jsonify({
                "erro": "Nao foi possivel consultar os materiais."
            }), 503

    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({"erro": "Envie um JSON valido."}), 400

    nome = str(dados.get("nome_material") or "").strip()

    try:
        total = int(dados["qtd_total"])
        disponivel = int(dados["qtd_disponivel"])
        categoria = int(dados["id_categoria"])
        localizacao = int(dados["id_localizacao"])

    except (KeyError, ValueError, TypeError):
        return jsonify({
            "erro": "Informe quantidades, categoria e localizacao."
        }), 400

    if (
        not nome
        or total < 0
        or disponivel < 0
        or disponivel > total
        or categoria <= 0
        or localizacao <= 0
    ):
        return jsonify({
            "erro": "Dados do material invalidos."
        }), 400

    material = Material(
        nome_material=nome,
        qtd_total=total,
        qtd_disponivel=disponivel,
        id_categoria=categoria,
        id_localizacao=localizacao
    )

    try:
        MaterialDAO.cadastrar(material)

    except pymysql.IntegrityError:
        return jsonify({
            "erro": "Categoria, localizacao ou dados invalidos."
        }), 409

    except pymysql.MySQLError:
        return jsonify({
            "erro": "Nao foi possivel cadastrar o material."
        }), 503

    return jsonify(material.para_dict()), 201


# ROTAS DE RESERVAS

@app.route("/api/reservas", methods=["GET", "POST"])
def reservas():

    # CONSULTAR RESERVAS
    if request.method == "GET":
        try:
            lista = ReservaDAO.listar_todos()

            return jsonify([
                reserva.para_dict()
                for reserva in lista
            ])

        except pymysql.MySQLError:
            return jsonify({
                "erro": "Nao foi possivel consultar as reservas."
            }), 503

    # CADASTRAR RESERVA
    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({
            "erro": "Envie um JSON valido."
        }), 400

    try:
        id_usuario = int(dados["id_usuario"])

        data_solicitacao = date.fromisoformat(
            dados["data_solicitacao"]
        )

        data_retirada = date.fromisoformat(
            dados["data_previsao_retirada"]
        )

    except (KeyError, ValueError, TypeError):
        return jsonify({
            "erro": "Usuario ou datas invalidas."
        }), 400

    if id_usuario <= 0 or data_retirada < data_solicitacao:
        return jsonify({
            "erro": "Verifique o usuario e as datas."
        }), 400

    reserva = Reserva(
        id_usuario=id_usuario,
        data_solicitacao=data_solicitacao.isoformat(),
        data_previsao_retirada=data_retirada.isoformat()
    )

    try:
        ReservaDAO.cadastrar(reserva)

    except pymysql.IntegrityError:
        return jsonify({
            "erro": "Usuario inexistente ou dados invalidos."
        }), 409

    except pymysql.MySQLError:
        return jsonify({
            "erro": "Nao foi possivel cadastrar a reserva."
        }), 503

    return jsonify(reserva.para_dict()), 201


if __name__ == "__main__":
    app.run(debug=True)