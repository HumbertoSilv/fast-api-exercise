#!/bin/sh

# Executa as migrações do banco de dados
poetry run alembic upgrade head

# Inicia a aplicação
poetry run fastapi dev fast_api_exercise/app.py --host 0.0.0.0
# poetry run uvicorn --host 0.0.0.0 --port 8000 fast_api_exercise.app:app