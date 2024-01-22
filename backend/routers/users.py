from fastapi import APIRouter, HTTPException
from backend.schemas import Message, UserCreate, UserPublic, User, UserList, UserUpdate

router = APIRouter(
    prefix="/users",
    tags=["users"],
    # dependencies=[Depends(get_token_header)],
    # responses={404: {"description": "Not found"}}, # Em rotas em busca
)

database = []  # provisório para estudo!


@router.get('/', status_code=200, response_model=UserList)
def read_users():
    return {'users': database}


@router.post("/", status_code=201, response_model=UserPublic, tags=["users"])
def create_user(user: UserCreate):
    user_with_id = User(**user.model_dump(), id=len(database) + 1)
    database.append(user_with_id)

    return user_with_id


@router.put('/{user_id}', response_model=UserPublic)
def update_user(user_id: int, user: UserUpdate):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(status_code=404, detail='User not found')

    user_with_id = User(**user.model_dump(), id=user_id)
    database[user_id - 1] = user_with_id

    return user_with_id


@router.delete('/{user_id}', response_model=Message)
def delete_user(user_id: int):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(status_code=404, detail='User not found')

    del database[user_id - 1]

    return {'detail': 'User deleted'}
