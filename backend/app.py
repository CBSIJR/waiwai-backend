import uvicorn

from backend.configs import Settings


def start():
    settings: Settings = Settings()
    uvicorn.run('backend.waiwai:app', **settings.deployment())
