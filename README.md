# WaiWaiTapota API 2.0
TODO: Add description

## API Documentation
TODO: Add documentation

### Requisitos 
- [Python 3.11.x](https://www.python.org/)
- [Poetry 1.7.x](https://python-poetry.org/)
- [PostgreSQL 16.1](https://www.postgresql.org/)
#### Opcional
- [Docker *](https://www.docker.com/)

### Instalação
Configurando ambiente do Poetry:
```shell
$ poetry config virtualenvs.path .venv
$ poetry config settings.virtualenvs.in-project true
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
### Configurando
Baseado no arquivo de configuração de exemplo (`.env.sample`) você deverá criar um arquivo de configuração `.env` próprio para o seu ambiente.
Veja um exemplo abaixo:
```shell
[environment]
ENVIRONMENT=dev

[socket-binding]
HOST=0.0.0.0
PORT=8000

[development]
RELOAD=1

[production]
WORKERS=1

[logging]
LOG_LEVEL=info

[database]
DB_URL=postgres://postgres@localhost:5432/kwargs_db
DB_USER=postgres
DB_PASSWORD=postgres
```
### Iniciando 
Parar iniciar o projeto, basta executar o seguinte comando no seu terminal:
```shell
$ poetry run app
INFO:     Will watch for changes in these directories: ['/path/to/waiwai-backend/backend']
INFO:     Uvicorn running on http://127.0.0.1:8080 (Press CTRL+C to quit)
INFO:     Started reloader process [9999] using StatReload
INFO:     Started server process [9998]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```


### API Endpoints
TODO: Add endpoints
