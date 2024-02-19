from pydantic import BaseModel, Field, field_validator

from .base import Base


class Category(Base):
    category: str
    description: str


class CategoryPublic(Category):
    pass


class CategoryCreate(BaseModel):
    category: str = Field(min_length=3, max_length=20)
    description: str = Field(min_length=3, max_length=255)

    @field_validator('category')
    def first_name_alphanumeric(cls, v: str):
        assert v.isalnum(), 'Deve ser alfanumérico.'
        return v.capitalize()


class CategoryUpdate(CategoryCreate):
    pass
