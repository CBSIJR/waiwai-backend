import enum

from sqlalchemy import Column, ForeignKey, Table
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase

# https://stackoverflow.com/questions/75430842/is-it-possible-to-prevent-circular-imports-in-sqlalchemy-and-still-have-models-i
# https://stackoverflow.com/questions/75919378/how-to-handle-circular-imports-in-sqlalchemy


class PermissionType(str, enum.Enum):
    GUEST = 'GUEST'
    USER = 'USER'
    ADMIN = 'ADMIN'


class WordStatus(enum.Enum):
    """
    Máquina de estados para controle de aprovação de palavras.

    Fluxo:
        - ADMIN cria → direto para APPROVED.
        - USER cria  → começa em PENDING.
        - ADMIN revisa → move para APPROVED, REJECTED ou CHANGES_REQUESTED.
    """
    PENDING = 'PENDING'
    APPROVED = 'APPROVED'
    REJECTED = 'REJECTED'
    CHANGES_REQUESTED = 'CHANGES_REQUESTED'


class Base(AsyncAttrs, DeclarativeBase):
    pass


WordCategory = Table(
    'word_category',
    Base.metadata,
    Column('word_id', ForeignKey('words.id'), primary_key=True),
    Column('category_id', ForeignKey('categories.id'), primary_key=True),
)
