from banco import obter_conexao
from modelo import (
    Usuario, Material, Reserva, Emprestimo,
    ItemEmprestimo, ItemReserva
)

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



class ItemEmprestimoDAO:

    @staticmethod
    def registrar_emprestimo(emprestimo, item):

        if (
            not isinstance(item.quantidade_emprestada, int)
            or item.quantidade_emprestada <= 0
        ):
            raise ValueError("A quantidade deve ser positiva.")

        conexao = obter_conexao()

        try:
            conexao.begin()

            with conexao.cursor() as cursor:

                # 1. Consultar e bloquear o material
                cursor.execute("""
                    SELECT qtd_disponivel
                    FROM MATERIAL
                    WHERE id_material = %s
                    FOR UPDATE
                """, (item.id_material,))

                material = cursor.fetchone()

                if material is None:
                    raise ValueError("Material nao encontrado.")

                # 2. Verificar disponibilidade
                if material["qtd_disponivel"] < item.quantidade_emprestada:
                    raise ValueError("Estoque insuficiente.")

                # 3. Criar o empréstimo
                cursor.execute("""
                    INSERT INTO EMPRESTIMO
                    (id_usuario_solicitante, id_reserva,
                     data_retirada, data_previsao_devolucao,
                     data_devolucao)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    emprestimo.id_usuario_solicitante,
                    emprestimo.id_reserva,
                    emprestimo.data_retirada,
                    emprestimo.data_previsao_devolucao,
                    None
                ))

                novo_id = cursor.lastrowid

                # 4. Registrar o material emprestado
                cursor.execute("""
                    INSERT INTO ITEM_EMPRESTIMO
                    (id_emprestimo, id_material,
                     quantidade_emprestada, status_emprestimo)
                    VALUES (%s, %s, %s, %s)
                """, (
                    novo_id,
                    item.id_material,
                    item.quantidade_emprestada,
                    item.status_emprestimo
                ))

                novo_id_item = cursor.lastrowid

                # 5. Diminuir a quantidade disponível
                cursor.execute("""
                    UPDATE MATERIAL
                    SET qtd_disponivel = qtd_disponivel - %s
                    WHERE id_material = %s
                """, (
                    item.quantidade_emprestada,
                    item.id_material
                ))

            # 6. Confirmar todas as alterações
            conexao.commit()

            emprestimo.id_emprestimo = novo_id
            item.id_emprestimo = novo_id
            item.id_item_emprestimo = novo_id_item

            return novo_id

        except Exception:
            conexao.rollback()
            raise

        finally:
            conexao.close()





    @staticmethod
    def registrar_devolucao(id_item_emprestimo, estado_devolucao="bom"):

        # Por enquanto, devolvemos ao estoque apenas itens em bom estado.
        if estado_devolucao != "bom":
            raise ValueError(
                "Devolucoes com avarias serao tratadas separadamente."
            )

        if (
            not isinstance(id_item_emprestimo, int)
            or id_item_emprestimo <= 0
        ):
            raise ValueError("ID do item invalido.")

        conexao = obter_conexao()

        try:
            conexao.begin()

            with conexao.cursor() as cursor:

                # 1. Buscar o item e bloquear seu registro
                cursor.execute("""
                    SELECT id_emprestimo, id_material,
                           quantidade_emprestada, status_emprestimo
                    FROM ITEM_EMPRESTIMO
                    WHERE id_item_emprestimo = %s
                    FOR UPDATE
                """, (id_item_emprestimo,))

                item = cursor.fetchone()

                if item is None:
                    raise ValueError("Item emprestado nao encontrado.")

                # 2. Impedir devolucao duplicada
                if item["status_emprestimo"] != "emprestado":
                    raise ValueError("Este item ja foi devolvido.")

                quantidade = item["quantidade_emprestada"]
                id_material = item["id_material"]
                id_emprestimo = item["id_emprestimo"]

                # 3. Repor o estoque
                cursor.execute("""
                    UPDATE MATERIAL
                    SET qtd_disponivel = qtd_disponivel + %s
                    WHERE id_material = %s
                      AND qtd_disponivel + %s <= qtd_total
                """, (quantidade, id_material, quantidade))

                if cursor.rowcount != 1:
                    raise ValueError(
                        "Nao foi possivel atualizar o estoque."
                    )

                # 4. Marcar o item como devolvido
                cursor.execute("""
                    UPDATE ITEM_EMPRESTIMO
                    SET status_emprestimo = 'devolvido',
                        estado_devolucao = %s
                    WHERE id_item_emprestimo = %s
                """, (estado_devolucao, id_item_emprestimo))

                # 5. Registrar a data quando todos os itens voltarem
                cursor.execute("""
                    UPDATE EMPRESTIMO
                    SET data_devolucao = CURDATE()
                    WHERE id_emprestimo = %s
                      AND NOT EXISTS (
                          SELECT 1
                          FROM ITEM_EMPRESTIMO
                          WHERE id_emprestimo = %s
                            AND status_emprestimo <> 'devolvido'
                      )
                """, (id_emprestimo, id_emprestimo))

            # 6. Confirmar a devolucao
            conexao.commit()
            return True

        except Exception:
            conexao.rollback()
            raise

        finally:
            conexao.close()


class ItemReservaDAO:

    @staticmethod
    def cadastrar_reserva_com_item(reserva, item):

        if (
            not isinstance(item.qtd_reserva, int)
            or isinstance(item.qtd_reserva, bool)
            or item.qtd_reserva <= 0
            or not isinstance(item.id_material, int)
            or item.id_material <= 0
        ):
            raise ValueError("Material ou quantidade invalida.")

        conexao = obter_conexao()

        try:
            conexao.begin()

            with conexao.cursor() as cursor:

                # 1. Verificar se o material existe
                cursor.execute("""
                    SELECT qtd_disponivel
                    FROM MATERIAL
                    WHERE id_material = %s
                """, (item.id_material,))

                material = cursor.fetchone()

                if material is None:
                    raise ValueError("Material nao encontrado.")

                # 2. Consultar a disponibilidade atual
                if item.qtd_reserva > material["qtd_disponivel"]:
                    raise ValueError("Quantidade indisponivel.")

                # 3. Criar a reserva
                cursor.execute("""
                    INSERT INTO RESERVA
                    (id_usuario, data_solicitacao,
                     data_previsao_retirada, status_reserva)
                    VALUES (%s, %s, %s, %s)
                """, (
                    reserva.id_usuario,
                    reserva.data_solicitacao,
                    reserva.data_previsao_retirada,
                    "pendente"
                ))

                id_reserva = cursor.lastrowid

                # 4. Cadastrar o material da reserva
                cursor.execute("""
                    INSERT INTO ITEM_RESERVA
                    (id_reserva, id_material, qtd_reserva)
                    VALUES (%s, %s, %s)
                """, (
                    id_reserva,
                    item.id_material,
                    item.qtd_reserva
                ))

                id_item_reserva = cursor.lastrowid

            # 5. Confirmar os dois cadastros
            conexao.commit()

            reserva.id_reserva = id_reserva
            reserva.status_reserva = "pendente"
            item.id_reserva = id_reserva
            item.id_item_reserva = id_item_reserva

            return id_reserva

        except Exception:
            conexao.rollback()
            raise

        finally:
            conexao.close()
