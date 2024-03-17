from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from backend.auth import Authorization, JWTBearer
from backend.configs import get_async_session
from backend.repositories import References
from backend.schemas import (
    Message,
    ParamsReference,
    PermissionType,
    ReferenceCreate,
    ReferencePublic,
    ReferenceUpdate,
)

router = APIRouter(
    prefix='/references',
    tags=['Referências'],
)
security = JWTBearer()


@router.get(
    '/', status_code=status.HTTP_200_OK, response_model=list[ReferencePublic]
)
async def list_references(
    params: ParamsReference = Depends(),
    session: AsyncSession = Depends(get_async_session),
):
    references = await References(session).get_list(params)
    return references


@router.get(
    '/{reference_id}',
    status_code=status.HTTP_200_OK,
    responses={'404': {'model': Message}},
    response_model=ReferencePublic,
)
async def get_reference(
    reference_id: int, session: AsyncSession = Depends(get_async_session)
):
    reference = await References(session).get_by_id(reference_id)
    return reference


@router.post(
    '/',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(security),
        Authorization([PermissionType.ADMIN]),
    ],
    responses={'403': {'model': Message}, '409': {'model': Message}},
)
async def create_reference(
    reference: ReferenceCreate,
    session: AsyncSession = Depends(get_async_session),
) -> None:
    await References(session).create(reference)


@router.put(
    '/{reference_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(security),
        Authorization([PermissionType.ADMIN]),
    ],
    responses={
        '403': {'model': Message},
        '404': {'model': Message},
        '409': {'model': Message},
    },
)
async def update_reference(
    reference_id: int,
    reference: ReferenceUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    await References(session).update_by_id(reference_id, reference)


@router.delete(
    '/{reference_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[
        Depends(security),
        Authorization([PermissionType.ADMIN]),
    ],
    responses={
        '403': {'model': Message},
        '404': {'model': Message},
        '409': {'model': Message},
    },
)
async def delete_reference(
    reference_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    await References(session).delete_by_id(reference_id)
