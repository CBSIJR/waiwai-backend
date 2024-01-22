from backend.configs import Settings
import uvicorn


def start():
    settings: Settings = Settings()
    uvicorn.run("backend.waiwai:app", **settings.deployment())
