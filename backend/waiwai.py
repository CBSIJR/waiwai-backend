from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from backend.routers import (
    auth,
    categories,
    meanings,
    references,
    wordmeanings,
    words,
    worduploads,
)

app = FastAPI(
    redoc_url=None,
    title='WaiWaiTapota API',
    summary='Serviço de API do Dicionário WaiWai - UFOPA',
)

app.include_router(auth)
app.include_router(words)
app.include_router(wordmeanings)
app.include_router(meanings)
app.include_router(categories)
app.include_router(references)
app.include_router(worduploads)
app.mount('/uploads', StaticFiles(directory='backend/files'), 'files')


@app.get('/', tags=['Health'])
def health() -> dict:
    return {'message': 'hello'}
