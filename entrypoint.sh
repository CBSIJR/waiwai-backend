#!/bin/sh
set -e

echo "➡️  Rodando as migrations do banco de dados (Alembic)..."
# Executa as migrations para garantir que a tabela tenha todas as colunas
poetry run alembic upgrade head

echo "➡️  Iniciando a API FastAPI..."
# Executa a aplicação usando o comando do poetry
exec poetry run app
