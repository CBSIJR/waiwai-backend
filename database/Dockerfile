FROM postgres:16.1

# Instalar o cron
RUN apt-get update && apt-get install -y cron

# Copiar o script de backup para o contêiner
COPY backup_db.sh /usr/local/bin/backup_db.sh
RUN chmod +x /usr/local/bin/backup_db.sh

# Configurar o cron job
RUN echo "0 2 * * * /usr/local/bin/backup_db.sh >> /var/log/backup.log 2>&1" | crontab -

# Criar diretório para backups
RUN mkdir -p /backups

RUN localedef -i pt_BR -c -f UTF-8 -A /usr/share/locale/locale.alias pt_BR.UTF-8
ENV LANG pt_BR.UTF-8

# Comando para iniciar o cron e o PostgreSQL
CMD ["sh", "-c", "cron && docker-entrypoint.sh postgres"]