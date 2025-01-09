## Aplicação de gerenciamento de TODO's em FastApi e Postgres

- ### **Descrição:**
    Uma simples aplicação web para fins didáticos que implementa funcionalidades de criação de usuários, autenticação e autorização e registro de TODO's.

- ### **Principais Funcionalidades:**
    - Registro, autenticação e autorização de usuários.
    - Listar, filtrar, atualizar e deletar usuários.
    - Usuário fazer registro, listagem, atualização e deleção de TODO's.

- ### **Tecnologias:**
    - **[FastAPI](https://fastapi.tiangolo.com/)**: Framework de desenvolvimento web para Python, que permite criar APIs de alto desempenho de forma eficiente e com menos código.
    - **[Docker](https://www.docker.com/)**: Para criar um ambiente isolado e replicável para aplicação, facilitando tanto o desenvolvimento quanto o deploy em produção.
    - **[SQLAlchemy](https://www.sqlalchemy.org/)**: Para a comunicação com o banco de dados, e o [Alembic](https://alembic.sqlalchemy.org/en/latest/) para gerenciar as migrações de banco de dados.
    - **[Poetry](https://python-poetry.org/)**: Gerenciador de pacotes e dependências.
    - **[Ruff](https://docs.astral.sh/ruff/)**: Um linter e formatador de código Python extremamente rápido, escrito em Rust.
    - **[Taskipy](https://github.com/taskipy/taskipy)**: Executor de tarefas.
    - **[Pydantic](https://docs.pydantic.dev/latest/)**: Biblioteca de validação de dados mais amplamente utilizada para Python.
    - **[PyJWT](https://pyjwt.readthedocs.io/en/stable/)**: Biblioteca Python que permite codificar e decodificar JSON Web Tokens (JWT).
    - **[Pytest](https://docs.pytest.org/en/stable/)**: Framework de testes.
    - **[Testcontainers](https://testcontainers.com/)**: Framework para manipular ambiente de testes.

    Além de conceitos e padrões como  TDD, CI/CD...

## Como rodar a aplicação:
A aplicação foi construída usando Docker Compose, então basta ter o mesmo instalado na maquina e executar o comando:

```bash
   $ docker compose up
```

### **TODO de novas implementações:**

- [ ] Otimização de alguns testes usando parametrização (https://docs.pytest.org/en/stable/example/parametrize.html)
- [ ] Implementar Asyncio


