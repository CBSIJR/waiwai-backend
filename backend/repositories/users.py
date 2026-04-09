from datetime import datetime, timezone, timedelta
from typing import Sequence

from fastapi import status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from backend.auth import get_password_hash, sign_jwt, verify_password
from backend.models import User
from backend.schemas import (
    CustomHTTPException,
    Params,
    PermissionType,
    Subject,
    Token,
    UserCreate,
    UserLogin,
)

from .base import Repository


class Users(Repository):
    def __init__(self, session: AsyncSession) -> None:
        super().__init__()
        self.session: AsyncSession = session

    async def get_list(self, params: Params) -> Sequence[User]:
        statement = (
            select(User)
            .offset((params.page - 1) * params.page_size)
            .limit(params.page_size)
        )
        result = await self.session.execute(statement)
        users = result.scalars().all()
        return users

    async def create(self, entity: UserCreate) -> Token:
        user_db = await self.get_by_email(entity.email)

        if user_db:
            raise CustomHTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Email já registrado.',
            )

        hashed_password = get_password_hash(entity.password)

        user_db = User(
            first_name=entity.first_name,
            last_name=entity.last_name,
            full_name=entity.first_name + ' ' + entity.last_name,
            email=entity.email,
            password=hashed_password,
        )

        self.session.add(user_db)
        await self.session.commit()
        return sign_jwt(
            Subject(
                name=user_db.full_name,
                email=user_db.email,
                permission=user_db.permission,
            )
        )

    async def get_by_id(self, entity_id: int) -> User | None:
        statement = select(User).filter(User.id == entity_id)
        result = await self.session.execute(statement)
        user = result.scalar_one_or_none()
        return user

    async def get_by_email(self, entity_email: str) -> User | None:
        statement = select(User).where(User.email == entity_email)
        result = await self.session.execute(statement)
        user = result.scalar_one_or_none()
        return user

    async def update_by_id(
        self, entity_id: int, entity: User, user: User
    ) -> None:
        user_db = await self.get_by_id(entity_id)
        if user_db:
            raise CustomHTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='Não encontrado.'
            )

        user_db = self.get_by_email(entity.email)
        if user_db:
            raise CustomHTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='Email já registrado.',
            )

        user_db = User(
            first_name=entity.first_name,
            last_name=entity.last_name,
            full_name=entity.full_name,
            email=entity.email,
            password=entity.password,
            permission=entity.permission,
        )

        self.session.add(user_db)
        await self.session.commit()

    async def update_role(
        self, user_id: int, new_permission: PermissionType, current_user: Subject
    ) -> User:
        user_db = await self.get_by_id(user_id)
        if not user_db:
            raise CustomHTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail='Usuário não encontrado.'
            )

        # Bloqueia auto-moderação (não pode mudar o próprio cargo)
        if user_db.email == current_user.email:
            raise CustomHTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Você não pode alterar sua própria permissão.',
            )

        # Regra de Segurança: Rebaixamento (ADMIN -> USER)
        if user_db.permission == PermissionType.ADMIN and new_permission != PermissionType.ADMIN:
            now = datetime.now(timezone.utc)
            # Se o usuário não tem update_at (registros antigos) ou se já passou 24h
            if not user_db.update_at:
                 raise CustomHTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail='Este administrador é antigo e não pode ser rebaixado.'
                )
            
            # Garante que update_at tem timezone para comparação
            updated_at = user_db.update_at
            if updated_at.tzinfo is None:
                updated_at = updated_at.replace(tzinfo=timezone.utc)

            if (now - updated_at) > timedelta(days=1):
                raise CustomHTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail='Administradores só podem ser rebaixados dentro de 24h após a última alteração.'
                )

        user_db.permission = new_permission
        # O SQLAlchemy atualizará o update_at automaticamente se configurado no modelo,
        # mas forçamos o commit para garantir a persistência imediata.
        await self.session.commit()
        await self.session.refresh(user_db)
        return user_db

    async def delete_by_id(self, entity_id, entity: User) -> None:
        pass

    async def create_jwt(self, entity: UserLogin) -> Token:
        user_db = await self.get_by_email(entity.email)
        if not user_db:
            raise CustomHTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Email ou senha incorreto.',
            )

        if not verify_password(entity.password, user_db.password):
            raise CustomHTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Email ou senha incorreto.',
            )

        return sign_jwt(
            Subject(
                name=user_db.full_name,
                email=user_db.email,
                permission=user_db.permission,
            )
        )

    async def all(self) -> Sequence[User]:
        statement = select(User)

        result = await self.session.execute(statement)
        users = result.scalars().all()
        return users
