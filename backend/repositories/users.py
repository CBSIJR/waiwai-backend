from typing import Sequence

from fastapi import HTTPException, status

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models import User
from backend.repositories import Repository
from backend.schemas import Params, UserCreate, UserLogin, Token, Subject
from backend.auth import get_password_hash, verify_password, sign_jwt


class Users(Repository):
    def __init__(self, session: Session) -> None:
        super().__init__()
        self.session: Session = session

    async def get_list(self, params: Params) -> Sequence[User]:

        users = self.session.scalars(select(User)
                                     .offset((params.page - 1) * params.page_size)
                                     .limit(params.page_size)).all()
        return users

    async def create(self, entity: UserCreate) -> Token:
        user_db = await self.get_by_email(entity.email)

        if user_db:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='Email already registered'
            )

        hashed_password = get_password_hash(entity.password)

        user_db = User(
            first_name=entity.first_name,
            last_name=entity.last_name,
            full_name=entity.first_name + ' ' + entity.last_name,
            email=entity.email,
            password=hashed_password
        )

        self.session.add(user_db)
        self.session.commit()
        self.session.refresh(user_db)

        return sign_jwt(Subject(name=user_db.full_name, email=user_db.email))

    async def get_by_id(self, entity_id: int) -> User:
        return self.session.scalar(
            select(User).where(User.id == entity_id)
        )

    async def get_by_email(self, entity_email: str) -> User:
        return self.session.scalar(
            select(User).where(User.email == entity_email)
        )

    async def update_by_id(self, entity_id: int, entity: User, user: User) -> None:
        user_db = self.get_by_id(entity_id)
        if user_db:
            raise HTTPException(
                status_code=400, detail='Not found'
            )

        user_db = self.get_by_email(entity.email)
        if user_db:
            raise HTTPException(
                status_code=400, detail='Username already registered'
            )

        user_db = User(
            first_name=entity.first_name,
            last_name=entity.last_name,
            full_name=entity.full_name,
            email=entity.email,
            password=entity.password,
            permission=entity.permission
        )

        self.session.add(user_db)
        self.session.commit()
        self.session.refresh(user_db)

    async def delete_by_id(self, entity_id, entity: User) -> None:
        pass

    async def create_jwt(self, entity: UserLogin) -> Token:

        user_db = self.session.scalar(select(User).where(User.email == entity.email))

        if not user_db:
            raise HTTPException(
                status_code=400, detail='Incorrect email or password'
            )

        if not verify_password(entity.password, user_db.password):
            raise HTTPException(
                status_code=400, detail='Incorrect email or password'
            )

        return sign_jwt(Subject(name=user_db.full_name, email=user_db.email))
