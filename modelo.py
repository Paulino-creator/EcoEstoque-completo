
import json


class Usuario:
    def __init__(self, nome_usuario, tipo_usuario,
                 email="", matricula="", cpf="", id_usuario=None):

        self.id_usuario = id_usuario
        self.nome_usuario = nome_usuario
        self.tipo_usuario = tipo_usuario
        self.email = email
        self.matricula = matricula
        self.cpf = cpf

    def para_dict(self):
        return {
            "id_usuario": self.id_usuario,
            "nome_usuario": self.nome_usuario,
            "tipo_usuario": self.tipo_usuario,
            "email": self.email,
            "matricula": self.matricula,
            "cpf": self.cpf
        }


class Material:
    def __init__(self, nome_material, qtd_total,
                 qtd_disponivel, id_categoria, id_localizacao,
                 id_material=None):

        self.id_material = id_material
        self.nome_material = nome_material
        self.qtd_total = qtd_total
        self.qtd_disponivel = qtd_disponivel
        self.id_categoria = id_categoria
        self.id_localizacao = id_localizacao

    def para_dict(self):
        return {
            "id_material": self.id_material,
            "nome_material": self.nome_material,
            "qtd_total": self.qtd_total,
            "qtd_disponivel": self.qtd_disponivel,
            "id_categoria": self.id_categoria,
            "id_localizacao": self.id_localizacao
        }



class Reserva:
    def __init__(self, id_usuario, data_solicitacao,
                 data_previsao_retirada, status_reserva="pendente",
                 id_reserva=None):

        self.id_reserva = id_reserva
        self.id_usuario = id_usuario
        self.data_solicitacao = data_solicitacao
        self.data_previsao_retirada = data_previsao_retirada
        self.status_reserva = status_reserva

    def para_dict(self):
        return {
            "id_reserva": self.id_reserva,
            "id_usuario": self.id_usuario,
            "data_solicitacao": self.data_solicitacao,
            "data_previsao_retirada": self.data_previsao_retirada,
            "status_reserva": self.status_reserva
        }


class Emprestimo:
    def __init__(self, id_usuario_solicitante, data_retirada,
                 data_previsao_devolucao, id_reserva=None,
                 data_devolucao=None, id_emprestimo=None):

        self.id_emprestimo = id_emprestimo
        self.id_usuario_solicitante = id_usuario_solicitante
        self.id_reserva = id_reserva
        self.data_retirada = data_retirada
        self.data_previsao_devolucao = data_previsao_devolucao
        self.data_devolucao = data_devolucao

    def registrar_devolucao(self, data):
        if self.data_devolucao is not None:
            raise ValueError("Empréstimo já devolvido.")

        self.data_devolucao = data

    def para_dict(self):
        return {
            "id_emprestimo": self.id_emprestimo,
            "id_usuario_solicitante": self.id_usuario_solicitante,
            "id_reserva": self.id_reserva,
            "data_retirada": self.data_retirada,
            "data_previsao_devolucao": self.data_previsao_devolucao,
            "data_devolucao": self.data_devolucao
        }


