FROM python:3.13.10-alpine3.23 AS base

RUN pip install poetry==2.1.3

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

FROM base AS builder

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --without dev --no-root

FROM base AS runtime

RUN apk update && apk add dcron

COPY backup_public.sh /usr/local/bin/backup_public.sh
RUN chmod +x /usr/local/bin/backup_public.sh

# Optional: Add a cron job
RUN echo "*/5 * * * * /usr/local/bin/backup_public.sh >> /var/log/cron.log 2>&1" > /etc/crontabs/root
# Optional: Start crond in foreground
CMD ["dcron", "-f"]
# RUN echo "0 2 * * * /usr/local/bin/backup_public.sh >> /var/log/backup.log 2>&1" | crontab -

RUN mkdir -p /backups

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

WORKDIR /app

COPY . .

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

CMD ["/usr/local/bin/entrypoint.sh"]