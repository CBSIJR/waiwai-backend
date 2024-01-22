from pydantic import BaseModel, EmailStr


class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class User(UserCreate):
    id: int


class UserUpdate(UserCreate):
    pass


class UserList(BaseModel):
    users: list[UserPublic]
