from pydantic import BaseModel, EmailStr, Field, field_validator

from .base import Base, PermissionType


class User(Base):
    first_name: str
    last_name: str
    full_name: str
    email: str


class UserPublic(User):
    pass


class UserCreate(BaseModel):
    first_name: str = Field(min_length=3, max_length=15)
    last_name: str = Field(min_length=3, max_length=15)
    email: EmailStr
    password: str = Field(min_items=8, max_length=32)

    @field_validator('password', mode='before')
    def password_must_be_strong(cls, v: str):
        assert all(char.isalnum() for char in v
                   ), 'Deve conter apenas letras ou números.'
        assert any(
            char.isdigit() for char in v
        ), 'Deve conter pelo menos um dígito numérico.'
        assert any(
            char.isupper() for char in v
        ), 'Deve conter pelo menos uma letra maiúscula.'
        assert any(
            char.islower() for char in v
        ), 'Deve conter pelo menos uma letra minúscula.'
        return v

    @field_validator('first_name', 'last_name')
    def first_name_alphanumeric(cls, v: str):
        assert all(char.isalpha() for char in v), 'Deve conter apenas letras.'
        return v.capitalize()


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_items=8, max_length=32)


class UserAuth(Base):
    email: EmailStr
    permission: PermissionType


class UserUpdate(UserCreate):
    pass


class UserExport(Base):
    full_name: str
