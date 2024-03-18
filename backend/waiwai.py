from fastapi import FastAPI, status, Depends
from fastapi.staticfiles import StaticFiles
from sqlalchemy.ext.asyncio import AsyncSession

from backend.schemas import VersionPublic
from backend.repositories import Versions
from backend.configs import Settings, get_async_session
from backend.routers import (
    auth,
    categories,
    meanings,
    references,
    wordmeanings,
    words,
    wordattachments,
    attachments
)

settings = Settings()

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
app.include_router(wordattachments)
app.include_router(attachments)
app.mount('/uploads', StaticFiles(directory='backend/static'), 'static')


@app.get('/', tags=['Ping'])
def health() -> dict:
    return {'detail': 'hello world!'}


@app.get('/version',
         status_code=status.HTTP_200_OK,
         response_model=VersionPublic,
         tags=['Versão'])
async def get_version(session: AsyncSession = Depends(get_async_session)):
    version = await Versions(session).first()
    return version
