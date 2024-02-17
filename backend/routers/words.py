from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import status

from backend.configs import get_async_session
from backend.schemas import Message, Params, WordCreate, WordPublic, UserAuth
from backend.auth import security, get_current_user

from backend.repositories import Words

router = APIRouter(
    prefix="/words",
    tags=["Palavras"],
    # dependencies=[Depends(get_token_header)],
)


@router.get('/', status_code=status.HTTP_200_OK, response_model=list[WordPublic])
async def list_words(pagination: Params = Depends(), session: AsyncSession = Depends(get_async_session)):
    words = await Words(session).get_list(pagination)
    return words


@router.get('/{word_id}', status_code=status.HTTP_200_OK, response_model=WordPublic)
async def list_words(word_id: int, session: AsyncSession = Depends(get_async_session)):
    word = await Words(session).get_by_id(word_id)
    return word


@router.post('/', status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(security)],
             responses={403: {'model': Message}})
async def create_word(word: WordCreate, current_user: UserAuth = Depends(get_current_user),
                      session: AsyncSession = Depends(get_async_session)) -> None:
    await Words(session).create(word, current_user)
