FROM python:3.12.8-alpine3.21 AS base

RUN pip install poetry==1.8.4

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

FROM base AS builder

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --without dev --no-root

FROM base AS runtime

RUN apt-get update && apt-get install -y cron

COPY backup_public.sh /usr/local/bin/backup_public.sh
RUN chmod +x /usr/local/bin/backup_public.sh

RUN echo "0 2 * * * /usr/local/bin/backup_public.sh >> /var/log/backup.log 2>&1" | crontab -

RUN mkdir -p /backups

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

WORKDIR /app

COPY . .

CMD ["sh", "-c", "cron && poetry run app"]