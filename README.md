# WaiWaiTapota API 2.0

TODO: Add description

### Requisitos

- [Python 3.12.x](https://www.python.org/)
- [Poetry 1.7.x](https://python-poetry.org/)
- [PostgreSQL 16.1](https://www.postgresql.org/)

#### Opcional

- [Docker \*](https://www.docker.com/)

### Instalação Manual

Configurando ambiente do Poetry:

```shell
$ poetry config virtualenvs.path .venv
$ poetry config virtualenvs.in-project true
```

Clonando repositório:

```shell
$ git clone https://github.com/aejuniordev/waiwai-backend.git
```

Instalando dependências:

```shell
$ cd waiwai-backend
$ poetry install
```

### Instalação com Docker

```
$ docker build -t aejunior/waiwai-backend:latest .
$ docker network create -d bridge api_proxy
$ docker network create -d bridge api_db_migration
```

### Configurando certificado SSL 
```shell
$ docker exec -it <ID> sh
$ certbot --nginx
```

### Configurando

Baseado no arquivo de configuração de exemplo (`.env.sample`) você deverá criar um arquivo de configuração `.env` próprio para o seu ambiente.
Veja um exemplo abaixo:

```shell
[environment]
ENVIRONMENT=dev                 # dev or prod

[socket-binding]
HOST=0.0.0.0                    # Default: '127.0.0.1'
PORT=8080                       # Default: 8000

[development]
RELOAD=1

[production]
WORKERS=1                       # Default 1 for development
JWT_ALGORITHM=                  # Default: HS256
JWT_SECRET_KEY_ACCESS_TOKEN=    # https://randomkeygen.com/
JWT_SECRET_KEY_REFRESH_TOKEN=   # https://randomkeygen.com/
JWT_EXPIRATION_ACCESS_TOKEN=    # Default: 30
JWT_EXPIRATION_REFRESH_TOKEN=   # Default: 10080


[logging]
# LOG_CONFIG=                   # TODO
# NO_ACCESS_LOG=                # TODO
LOG_LEVEL=info

[database]
DB_URL=postgresql+asyncpg://<user>:<password>@<host>/<database>
```

### Restaurando Banco de dados

Para subir a última versão do banco de dados basta executar o seguinte comando na raiz do projeto:

```sh
$ alembic upgrade head
```

Obs.: Necessário ter uma instância do banco de dados (PostgreSQL) em execução e configurado no [Alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html).

### Iniciando

Parar iniciar o projeto, basta executar o seguinte comando no seu terminal:

```shell
$ poetry run app
```

Saída de execução:

```sheel
INFO:     Will watch for changes in these directories: ['/path/to/waiwai-backend/backend']
INFO:     Uvicorn running on http://127.0.0.1:8080 (Press CTRL+C to quit)
INFO:     Started reloader process [9999] using StatReload
INFO:     Started server process [9998]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

## API Documentation

TODO: Add documentation

### API Endpoints

TODO: Add endpoints

### Configurando CRON para renovação de certificado

Editar CRON tabs.
```sh
$ crontab -e
```
Incluir comando para renovação:
```sh
SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
0 */12 * * * root certbot -q renew --nginx
```