from pydantic import BaseModel, Field, field_validator

from .base import Base


class Category(Base):
    category: str
    description: str


class CategoryPublic(Category):
    pass

class CategoryExport(Category):
    pass


class CategoryCreate(BaseModel):
    category: str = Field(min_length=3, max_length=20)
    description: str = Field(min_length=3, max_length=255)

    @field_validator('category')
    def category_validator(cls, v: str):
        # Remove espaços extras no início/fim
        v = v.strip()

        # Substitui múltiplos espaços por apenas um
        v = ' '.join(v.split())

        assert all(c.isalpha() or c.isspace() for c in v), 'Deve conter apenas letras e espaços.'
        # assert v.isalpha() or v.isnumeric(), 'Deve ser alfabético.'
        return v.capitalize()

    @field_validator('description')
    def description_validator(cls, v: str):
        # Remove espaços extras no início/fim
        v = v.strip()

        # Substitui múltiplos espaços por apenas um
        v = ' '.join(v.split())

        return v.capitalize()


class CategoryUpdate(CategoryCreate):
    pass
