#!/bin/sh

# Executa as migrações do banco de dados
poetry run alembic upgrade head

# Inicia a aplicação
poetry run fastapi run fast_api_exercise/app.py
# poetry run uvicorn --host 0.0.0.0 fast_api_exercise.app:app