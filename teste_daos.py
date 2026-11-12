
from unittest.mock import MagicMock, patch

from modelo import Reserva, Emprestimo
from daos import ReservaDAO, EmprestimoDAO


# Criamos uma conexão falsa para os testes
conexao_falsa = MagicMock()
cursor_falso = (
    conexao_falsa.cursor.return_value.__enter__.return_value
)

# Simulamos a conexão sem acessar o MySQL
with patch("daos.obter_conexao", return_value=conexao_falsa):

    cursor_falso.lastrowid = 101

    reserva = Reserva(
        id_usuario=1,
        data_solicitacao="2026-11-11",
        data_previsao_retirada="2026-11-12"
    )

    ReservaDAO.cadastrar(reserva)

    print("Reserva simulada:", reserva.id_reserva)

    cursor_falso.lastrowid = 202

    emprestimo = Emprestimo(
        id_usuario_solicitante=1,
        id_reserva=101,
        data_retirada="2026-11-12",
        data_previsao_devolucao="2026-11-17"
    )

    EmprestimoDAO.cadastrar(emprestimo)

    print("Emprestimo simulado:", emprestimo.id_emprestimo)

    assert conexao_falsa.commit.call_count == 2

print("Testes de cadastro simulados concluidos!")
