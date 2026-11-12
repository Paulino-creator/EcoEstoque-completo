from banco import obter_conexao
from modelo import Usuario, Material, Reserva, Emprestimo


class UsuarioDAO:

    @staticmethod
    def cadastrar(usuario):
        conexao = obter_conexao()

        try:
            with conexao.cursor() as cursor:
                sql = """
                    INSERT INTO USUARIO
                    (nome_usuario, cpf, email, matricula, tipo_usuario)
                    VALUES (%s, %s, %s, %s, %s)
                """

                valores = (
                    usuario.nome_usuario,
                    usuario.cpf or None,
                    usuario.email or None,
                    usuario.matricula or None,
                    usuario.tipo_usuario
                )

                cursor.execute(sql, valores)
                usuario.id_usuario = cursor.lastrowid

            conexao.commit()
            return usuario.id_usuario

        finally:
            conexao.close()

    @staticmethod
    def listar_todos():
        conexao = obter_conexao()

        try:
            with conexao.cursor() as cursor:
                cursor.execute("SELECT * FROM USUARIO ORDER BY id_usuario")
                registros = cursor.fetchall()

            usuarios = []

            for registro in registros:
                usuario = Usuario(
                    nome_usuario=registro["nome_usuario"],
                    tipo_usuario=registro["tipo_usuario"],
                    email=registro["email"] or "",
                    matricula=registro["matricula"] or "",
                    cpf=registro["cpf"] or "",
                    id_usuario=registro["id_usuario"]
                )

                usuarios.append(usuario)

            return usuarios

        finally:
            conexao.close()


class MaterialDAO:

    @staticmethod
    def cadastrar(material):
        conexao = obter_conexao()

        try:
            with conexao.cursor() as cursor:
                sql = """
                    INSERT INTO MATERIAL
                    (nome_material, qtd_total, qtd_disponivel,
                     id_categoria, id_localizacao)
                    VALUES (%s, %s, %s, %s, %s)
                """

                valores = (
                    material.nome_material,
                    material.qtd_total,
                    material.qtd_disponivel,
                    material.id_categoria,
                    material.id_localizacao
                )

                cursor.execute(sql, valores)
                material.id_material = cursor.lastrowid

            conexao.commit()
            return material.id_material

        finally:
            conexao.close()

    @staticmethod
    def listar_todos():
        conexao = obter_conexao()

        try:
            with conexao.cursor() as cursor:
                cursor.execute("SELECT * FROM MATERIAL ORDER BY id_material")
                registros = cursor.fetchall()

            materiais = []

            for registro in registros:
                material = Material(
                    nome_material=registro["nome_material"],
                    qtd_total=registro["qtd_total"],
                    qtd_disponivel=registro["qtd_disponivel"],
                    id_categoria=registro["id_categoria"],
                    id_localizacao=registro["id_localizacao"],
                    id_material=registro["id_material"]
                )

                materiais.append(material)

            return materiais

        finally:
            conexao.close()




class ReservaDAO:

    @staticmethod
    def cadastrar(reserva):
        conexao = obter_conexao()

        try:
            with conexao.cursor() as cursor:
                sql = """
                    INSERT INTO RESERVA
                    (id_usuario, data_solicitacao,
                     data_previsao_retirada, status_reserva)
                    VALUES (%s, %s, %s, %s)
                """

                valores = (
                    reserva.id_usuario,
                    reserva.data_solicitacao,
                    reserva.data_previsao_retirada,
                    reserva.status_reserva
                )

                cursor.execute(sql, valores)
                novo_id = cursor.lastrowid

            conexao.commit()
            reserva.id_reserva = novo_id
            return novo_id

        except Exception:
            conexao.rollback()
            raise

        finally:
            conexao.close()

    @staticmethod
    def listar_todos():
        conexao = obter_conexao()

        try:
            with conexao.cursor() as cursor:
                cursor.execute("""
                    SELECT * FROM RESERVA
                    ORDER BY id_reserva DESC
                """)

                registros = cursor.fetchall()

            reservas = []

            for r in registros:
                reserva = Reserva(
                    id_usuario=r["id_usuario"],
                    data_solicitacao=str(r["data_solicitacao"]),
                    data_previsao_retirada=str(
                        r["data_previsao_retirada"]
                    ),
                    status_reserva=r["status_reserva"],
                    id_reserva=r["id_reserva"]
                )

                reservas.append(reserva)

            return reservas

        finally:
            conexao.close()

    @staticmethod
    def buscar_por_id(id_reserva):
        conexao = obter_conexao()

        try:
            with conexao.cursor() as cursor:
                cursor.execute("""
                    SELECT * FROM RESERVA
                    WHERE id_reserva = %s
                """, (id_reserva,))

                r = cursor.fetchone()

            if r is None:
                return None

            return Reserva(
                id_usuario=r["id_usuario"],
                data_solicitacao=str(r["data_solicitacao"]),
                data_previsao_retirada=str(
                    r["data_previsao_retirada"]
                ),
                status_reserva=r["status_reserva"],
                id_reserva=r["id_reserva"]
            )

        finally:
            conexao.close()


class EmprestimoDAO:

    @staticmethod
    def cadastrar(emprestimo):
        conexao = obter_conexao()

        try:
            with conexao.cursor() as cursor:
                sql = """
                    INSERT INTO EMPRESTIMO
                    (id_usuario_solicitante, id_reserva,
                     data_retirada, data_previsao_devolucao,
                     data_devolucao)
                    VALUES (%s, %s, %s, %s, %s)
                """

                valores = (
                    emprestimo.id_usuario_solicitante,
                    emprestimo.id_reserva,
                    emprestimo.data_retirada,
                    emprestimo.data_previsao_devolucao,
                    emprestimo.data_devolucao
                )

                cursor.execute(sql, valores)
                novo_id = cursor.lastrowid

            conexao.commit()
            emprestimo.id_emprestimo = novo_id
            return novo_id

        except Exception:
            conexao.rollback()
            raise

        finally:
            conexao.close()

    @staticmethod
    def listar_todos():
        conexao = obter_conexao()

        try:
            with conexao.cursor() as cursor:
                cursor.execute("""
                    SELECT * FROM EMPRESTIMO
                    ORDER BY id_emprestimo DESC
                """)

                registros = cursor.fetchall()

            emprestimos = []

            for e in registros:
                emprestimo = Emprestimo(
                    id_usuario_solicitante=(
                        e["id_usuario_solicitante"]
                    ),
                    id_reserva=e["id_reserva"],
                    data_retirada=str(e["data_retirada"]),
                    data_previsao_devolucao=str(
                        e["data_previsao_devolucao"]
                    ),
                    data_devolucao=(
                        str(e["data_devolucao"])
                        if e["data_devolucao"] is not None
                        else None
                    ),
                    id_emprestimo=e["id_emprestimo"]
                )

                emprestimos.append(emprestimo)

            return emprestimos

        finally:
            conexao.close()

    @staticmethod
    def buscar_por_id(id_emprestimo):
        conexao = obter_conexao()

        try:
            with conexao.cursor() as cursor:
                cursor.execute("""
                    SELECT * FROM EMPRESTIMO
                    WHERE id_emprestimo = %s
                """, (id_emprestimo,))

                e = cursor.fetchone()

            if e is None:
                return None

            return Emprestimo(
                id_usuario_solicitante=(
                    e["id_usuario_solicitante"]
                ),
                id_reserva=e["id_reserva"],
                data_retirada=str(e["data_retirada"]),
                data_previsao_devolucao=str(
                    e["data_previsao_devolucao"]
                ),
                data_devolucao=(
                    str(e["data_devolucao"])
                    if e["data_devolucao"] is not None
                    else None
                ),
                id_emprestimo=e["id_emprestimo"]
            )

        finally:
            conexao.close()
