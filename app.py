from datetime import date
from flask import Flask, jsonify, request
import pymysql

from modelo import (
    Usuario,
    Material,
    Reserva,
    Emprestimo,
    ItemEmprestimo,
    ItemReserva
)

from daos import (
    UsuarioDAO,
    MaterialDAO,
    ReservaDAO,
    EmprestimoDAO,
    ItemEmprestimoDAO,
    ItemReservaDAO
)

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
            return jsonify([r.para_dict() for r in lista])

        except pymysql.MySQLError:
            return jsonify({
                "erro": "Nao foi possivel consultar as reservas."
            }), 503

    # RECEBER DADOS
    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({
            "erro": "Envie um JSON valido."
        }), 400

    try:
        id_usuario = int(dados["id_usuario"])
        id_material = int(dados["id_material"])
        quantidade = int(dados["qtd_reserva"])

        solicitacao = date.fromisoformat(
            dados["data_solicitacao"]
        )

        previsao = date.fromisoformat(
            dados["data_previsao_retirada"]
        )

    except (KeyError, ValueError, TypeError):
        return jsonify({
            "erro": "Dados da reserva invalidos."
        }), 400

    # VALIDAR INFORMACOES
    if (
        id_usuario <= 0
        or id_material <= 0
        or quantidade <= 0
        or previsao < solicitacao
    ):
        return jsonify({
            "erro": "Verifique os IDs, a quantidade e as datas."
        }), 400

    # CRIAR OBJETO RESERVA
    reserva = Reserva(
        id_usuario=id_usuario,
        data_solicitacao=solicitacao.isoformat(),
        data_previsao_retirada=previsao.isoformat()
    )

    # CRIAR OBJETO ITEM_RESERVA
    item = ItemReserva(
        id_material=id_material,
        qtd_reserva=quantidade
    )

    # CADASTRAR NO BANCO
    try:
        ItemReservaDAO.cadastrar_reserva_com_item(
            reserva, item
        )

    except ValueError as erro:
        return jsonify({
            "erro": str(erro)
        }), 400

    except pymysql.IntegrityError:
        return jsonify({
            "erro": "Usuario ou material inexistente."
        }), 409

    except pymysql.MySQLError:
        return jsonify({
            "erro": "Nao foi possivel cadastrar a reserva."
        }), 503

    return jsonify({
        "mensagem": "Solicitacao de reserva registrada!",
        "reserva": reserva.para_dict(),
        "item": item.para_dict()
    }), 201


# ROTAS DE EMPRESTIMOS

@app.route("/api/emprestimos", methods=["GET", "POST"])
def emprestimos():

    # CONSULTAR EMPRESTIMOS
    if request.method == "GET":
        try:
            lista = EmprestimoDAO.listar_todos()

            return jsonify([
                emprestimo.para_dict()
                for emprestimo in lista
            ])

        except pymysql.MySQLError:
            return jsonify({
                "erro": "Nao foi possivel consultar os emprestimos."
            }), 503

    # CADASTRAR EMPRESTIMO
    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({
            "erro": "Envie um JSON valido."
        }), 400

    try:
        id_usuario = int(dados["id_usuario_solicitante"])
        id_material = int(dados["id_material"])
        quantidade = int(dados["quantidade_emprestada"])

        retirada = date.fromisoformat(
            dados["data_retirada"]
        )

        previsao = date.fromisoformat(
            dados["data_previsao_devolucao"]
        )

        id_reserva = dados.get("id_reserva")

        if id_reserva is not None:
            id_reserva = int(id_reserva)

    except (KeyError, ValueError, TypeError):
        return jsonify({
            "erro": "Dados do emprestimo invalidos."
        }), 400

    if (
        id_usuario <= 0
        or id_material <= 0
        or quantidade <= 0
        or previsao < retirada
        or (id_reserva is not None and id_reserva <= 0)
    ):
        return jsonify({
            "erro": "Verifique os IDs, a quantidade e as datas."
        }), 400

    emprestimo = Emprestimo(
        id_usuario_solicitante=id_usuario,
        id_reserva=id_reserva,
        data_retirada=retirada.isoformat(),
        data_previsao_devolucao=previsao.isoformat()
    )

    item = ItemEmprestimo(
        id_material=id_material,
        quantidade_emprestada=quantidade
    )

    try:
        ItemEmprestimoDAO.registrar_emprestimo(
            emprestimo, item
        )

    except ValueError as erro:
        return jsonify({
            "erro": str(erro)
        }), 400

    except pymysql.IntegrityError:
        return jsonify({
            "erro": "Usuario, material ou reserva invalida."
        }), 409

    except pymysql.MySQLError:
        return jsonify({
            "erro": "Nao foi possivel registrar o emprestimo."
        }), 503

    return jsonify({
        "mensagem": "Emprestimo registrado com sucesso!",
        "emprestimo": emprestimo.para_dict(),
        "item": item.para_dict()
    }), 201


# ROTAS DE DEVOLUCOES

@app.route("/api/devolucoes", methods=["POST"])
def devolucoes():

    dados = request.get_json(silent=True)

    if not isinstance(dados, dict):
        return jsonify({
            "erro": "Envie um JSON valido."
        }), 400

    try:
        id_item = int(dados["id_item_emprestimo"])

    except (KeyError, ValueError, TypeError):
        return jsonify({
            "erro": "ID do item invalido."
        }), 400

    if id_item <= 0:
        return jsonify({
            "erro": "ID do item deve ser positivo."
        }), 400

    estado = dados.get("estado_devolucao", "bom")

    if estado != "bom":
        return jsonify({
            "erro": "Avarias precisam de tratamento separado."
        }), 400

    try:
        ItemEmprestimoDAO.registrar_devolucao(
            id_item, estado
        )

    except ValueError as erro:
        return jsonify({
            "erro": str(erro)
        }), 400

    except pymysql.MySQLError:
        return jsonify({
            "erro": "Nao foi possivel registrar a devolucao."
        }), 503

    return jsonify({
        "mensagem": "Devolucao registrada com sucesso!",
        "id_item_emprestimo": id_item
    }), 200


if __name__ == "__main__":
    app.run(debug=True)