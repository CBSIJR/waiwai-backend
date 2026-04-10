from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.auth import Authorization, JWTBearer, get_current_user
from backend.configs import get_async_session
from backend.repositories import Users
from backend.schemas import (
    BaseResponse,
    PermissionType,
    UserAuth,
    UserPublic,
    UserRoleUpdate,
    ErrorResponse,
)

router = APIRouter(
    prefix='/users',
    tags=['Usuários'],
)
security = JWTBearer()


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(security), Authorization([PermissionType.ADMIN])],
    response_model=BaseResponse[List[UserPublic]],
    responses={'403': {'model': ErrorResponse}},
)
async def list_users(session: AsyncSession = Depends(get_async_session)):
    """
    Lista todos os usuários do sistema.
    Acesso restrito a ADMIN.
    """
    result = await Users(session).all()
    return BaseResponse[List[UserPublic]](data=result)


@router.patch(
    '/{user_id}/role',
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(security), Authorization([PermissionType.ADMIN])],
    response_model=BaseResponse[UserPublic],
    responses={
        '403': {'model': ErrorResponse},
        '404': {'model': ErrorResponse},
    },
)
async def update_user_role(
    user_id: int,
    role_update: UserRoleUpdate,
    current_user: UserAuth = Depends(get_current_user),
    session: AsyncSession = Depends(get_async_session),
):
    """
    Atualiza o cargo (permissão) de um usuário.
    Possui travas de segurança:
    - Não permite demotão de ADMIN após 24h.
    - Não permite auto-demotão.
    """
    result = await Users(session).update_role(
        user_id, role_update.permission, current_user
    )
    return BaseResponse[UserPublic](data=result)


@router.get(
    '/export/all',
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(security), Authorization([PermissionType.ADMIN])],
    # response_model=List[UserExport], # This was inconsistent with common patterns, but kept for legacy
)
async def get_export(session: AsyncSession = Depends(get_async_session)):
    users = await Users(session).all()
    return users
