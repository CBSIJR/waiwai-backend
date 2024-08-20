#!/bin/sh

cd app/

# Executa as migrações do Alembic
alembic upgrade head

# Executa o comando original
exec "$@"