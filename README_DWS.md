# EcoEstoque — Front-end DWS

Este pacote adiciona a interface em **HTML + CSS + JavaScript** ao repositório EcoEstoque. O arquivo `app.py` original **não precisa ser substituído**.

## Instalação no Mac (sem XAMPP)

1. Copie **todos** os arquivos deste pacote para a pasta do seu projeto `EcoEstoque-completo`. A pasta `frontend` precisa ficar ao lado de `app.py`, `modelo.py`, `daos.py` etc.
2. No Terminal do VS Code, dentro da pasta do projeto:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   python -m pip install -r requirements.txt
   python executar_demo.py
   ```

3. Abra **http://127.0.0.1:5001/painel** no navegador.
4. Teste: cadastrar usuário, cadastrar material, reservar, emprestar, devolver e conferir se a quantidade disponível aumenta de novo.
5. O servidor de demonstração grava alterações em `dados_demo.json`, que é ignorado pelo Git. Não é um banco MySQL.

Se a porta 5001 já estiver ocupada, encerre o outro Flask (`Ctrl+C` no terminal) antes de rodar.

## Teste integrado com MySQL / XAMPP

Quando estiver usando uma máquina com MySQL, abra **o mesmo projeto**, configure o `banco.py`, importe `estrutura.sql` e (se necessário) crie categorias e localizações antes de cadastrar materiais.

Execute `python executar_real.py` e abra **http://127.0.0.1:5001/painel**.

**Atenção:** em `executar_real.py`, as rotas de cadastro/consulta continuam usando os DAOs do seu `app.py` original. As rotas auxiliares de listagem de itens, categorias e localizações foram acrescentadas para completar a interface. O fluxo real ainda exige testes com MySQL e correção de eventuais erros.

## Arquivos

- `frontend/index.html`: estrutura das páginas e dos formulários.
- `frontend/styles.css`: estilo responsivo.
- `frontend/app.js`: chamadas `fetch`, navegação, formulários e atualização das tabelas.
- `executar_demo.py`: API demonstrativa com JSON no lugar de MySQL.
- `executar_real.py`: executa o `app.py` original e disponibiliza o front-end e rotas auxiliares de consulta.
- `teste_demo.py`: testes básicos do fluxo demonstrativo.
- `requirements.txt`: dependências.
- `.gitignore`: arquivos de ambiente e dados locais que não devem ser publicados.

## Roteiro rápido de apresentação

1. **DWS**: mostrar a interface, layout responsivo, tabelas e formulários.
2. **Fetch API**: abrir `frontend/app.js` e demonstrar que os botões enviam requisições para `/api/usuarios`, `/api/materiais`, `/api/reservas`, `/api/emprestimos` e `/api/devolucoes`.
3. **POO**: mostrar `modelo.py` e `daos.py`; explicar `Usuario`, `Material`, `Reserva`, `Emprestimo`, `ItemReserva`, `ItemEmprestimo` e transações com `commit`/`rollback`.
4. **Banco de Dados**: mostrar `estrutura.sql`, as tabelas e os relacionamentos.
5. **Demonstração**: cadastrar um usuário, reservar material, emprestar 1 unidade e devolver. O estoque reduz e aumenta novamente.

## Limitações (explicar ao professor com transparência)

- A demonstração local salva dados no **JSON**, não no MySQL; não vale como prova de integração com banco real.
- A reserva é pendente e **não bloqueia** estoque.
- O modelo implementado permite um item por pedido novo de reserva/empréstimo.
- Ainda não há autenticação/autorização de usuários, edição/exclusão nem tratamento de avarias para produção.
- A integração final com o MySQL precisa ser validada no ambiente escolar.
