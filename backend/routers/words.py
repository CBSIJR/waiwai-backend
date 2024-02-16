from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi import status

from backend.configs import get_session
from backend.schemas import Message, Params, WordCreate, WordPublic, UserAuth
from backend.auth import security, get_current_user

from backend.repositories import Words

router = APIRouter(
    prefix="/words",
    tags=["Palavras"],
    # dependencies=[Depends(get_token_header)],
)


@router.get('/', status_code=status.HTTP_200_OK, response_model=list[WordPublic])
async def list_words(pagination: Params = Depends(), session: Session = Depends(get_session)):
    words = await Words(session).get_list(pagination)
    return words


@router.post('/', status_code=status.HTTP_204_NO_CONTENT, dependencies=[Depends(security)],
             responses={403: {'model': Message}})
async def create_word(word: WordCreate, current_user: UserAuth = Depends(get_current_user),
                      session: Session = Depends(get_session)) -> None:
    await Words(session).create(word, current_user)
