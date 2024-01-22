from fastapi import FastAPI
from backend.routers import users


app = FastAPI()

app.include_router(users)


@app.get("/", tags=["Health"])
def health() -> dict:
    return {'message': 'hello'}
