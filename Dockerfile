FROM python:3.12.5-alpine3.20 AS base

RUN apk add --no-cache build-base curl gcc python3-dev musl-dev linux-headers

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

FROM base AS deps

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --only main

FROM base AS builder

WORKDIR /app

COPY --from=deps /root/.cache/pypoetry /root/.cache/pypoetry
COPY --from=deps /root/.local /root/.local

COPY . .

RUN poetry install --only main

FROM base AS runner

WORKDIR /app

COPY docker-entrypoint.sh /

COPY --from=builder /app /app
COPY --from=builder /root/.local /root/.local

ENV PATH="/root/.local/bin:$PATH"

EXPOSE 8080

ENTRYPOINT ["/docker-entrypoint.sh"]

CMD ["poetry", "run", "app"]