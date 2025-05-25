#!/bin/bash

# Configurações
BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d%H%M%S)
BACKUP_FILE="$BACKUP_DIR/$POSTGRES_DB_${DATE}.tar.gz"

# Realizar o backup
PGPASSWORD="$POSTGRES_PASSWORD" pg_dump -U "$POSTGRES_USER" -F t "$POSTGRES_DB" > "$BACKUP_FILE"

# Verificar se o backup foi bem-sucedido
if [ $? -eq 0 ]; then
    echo "Backup realizado com sucesso: $BACKUP_FILE"
    # Calcular o tamanho do arquivo de backup
    BACKUP_SIZE=$(du -h $BACKUP_FILE | awk '{print $1}')
    echo "Tamanho do backup: $BACKUP_SIZE"
else
    echo "Erro ao realizar o backup"
    exit 1
fi
