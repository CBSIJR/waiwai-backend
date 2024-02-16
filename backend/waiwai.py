from fastapi import FastAPI
from backend.routers import auth, words


app = FastAPI(redoc_url=None)

app.include_router(auth)
app.include_router(words)


@app.get("/", tags=["Health"])
def health() -> dict:
    return {'message': 'hello'}
