from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from backend.configs import Settings

engine = create_engine(str(Settings().db_url))


# https://github.com/tiangolo/fastapi/issues/2662
def get_session():
    with Session(engine) as session:
        yield session
