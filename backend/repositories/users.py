from typing import Sequence

from fastapi import HTTPException, status

from sqlalchemy import select, Row
from sqlalchemy.ext.asyncio import AsyncSession

from backend.models import User
from backend.repositories import Repository
from backend.schemas import Params, UserCreate, UserLogin, Token, Subject
from backend.auth import get_password_hash, verify_password, sign_jwt


class Users(Repository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__()
        self.session: AsyncSession = session

    async def get_list(self, params: Params) -> Sequence[Row[tuple[User]]]:
        statement = select(User).offset((params.page - 1) * params.page_size).limit(params.page_size)
        result = await self.session.execute(statement)
        users = result.all()
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
        await self.session.commit()
        await self.session.refresh(user_db)
        return sign_jwt(Subject(name=user_db.full_name, email=user_db.email))

    async def get_by_id(self, entity_id: int) -> User | None:
        statement = select(User).filter(User.id == entity_id)
        result = await self.session.execute(statement)
        return result.one_or_none()

    async def get_by_email(self, entity_email: str) -> User | None:
        statement = select(User).filter(User.email == entity_email)
        result = await self.session.execute(statement)
        return result.one_or_none()

    async def update_by_id(self, entity_id: int, entity: User, user: User) -> None:
        user_db = await self.get_by_id(entity_id)
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
        await self.session.commit()
        await self.session.refresh(user_db)

    async def delete_by_id(self, entity_id, entity: User) -> None:
        pass

    async def create_jwt(self, entity: UserLogin) -> Token:
        user_db = await self.get_by_email(entity.email)
        if not user_db:
            raise HTTPException(
                status_code=400, detail='Incorrect email or password'
            )

        if not verify_password(entity.password, user_db.password):
            raise HTTPException(
                status_code=400, detail='Incorrect email or password'
            )

        return sign_jwt(Subject(name=user_db.full_name, email=user_db.email))
