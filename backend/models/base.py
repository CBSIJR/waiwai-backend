import enum
from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy.orm import DeclarativeBase

# https://stackoverflow.com/questions/75430842/is-it-possible-to-prevent-circular-imports-in-sqlalchemy-and-still-have-models-i
# https://stackoverflow.com/questions/75919378/how-to-handle-circular-imports-in-sqlalchemy


class PermissionType(enum.Enum):
    GUEST = "GUEST"
    USER = "USER"
    ADMIN = "ADMIN"


class Base(DeclarativeBase):
    pass


WordCategory = Table(
    "word_category",
    Base.metadata,
    Column("word_id", ForeignKey("words.id"), primary_key=True),
    Column("category_id", ForeignKey("categories.id"), primary_key=True),
)
