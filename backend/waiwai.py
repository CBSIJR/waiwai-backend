from fastapi import FastAPI

from backend.routers import auth, words, categories

app = FastAPI(
    redoc_url=None,
    title='WaiWaiTapota API',
    summary='Serviço de API do Dicionário WaiWai - UFOPA',
)

app.include_router(auth)
app.include_router(words)
app.include_router(categories)


@app.get('/', tags=['Health'])
def health() -> dict:
    return {'message': 'hello'}
