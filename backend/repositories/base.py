from abc import abstractmethod, ABCMeta
from sqlalchemy.orm import DeclarativeBase
from pydantic import BaseModel
from typing import List


class Repository(metaclass=ABCMeta):
    """An interface to listing repository"""

    @abstractmethod
    async def create(self, entity: DeclarativeBase, user: BaseModel) -> None:
        """Adds new entity to a repository"""
        raise NotImplementedError()

    @abstractmethod
    async def get_list(self, params) -> List[DeclarativeBase]:
        """Removes existing entity from a repository"""
        raise NotImplementedError()

    @abstractmethod
    async def get_by_id(self, entity_id: int) -> DeclarativeBase:
        """Retrieves entity by its identity"""
        raise NotImplementedError()

    @abstractmethod
    async def update_by_id(self, entity_id: int, entity: DeclarativeBase, user: BaseModel) -> None:
        """Retrieves entity by its identity"""
        raise NotImplementedError()

    @abstractmethod
    async def delete_by_id(self, entity_id, user: BaseModel) -> None:
        """Retrieves entity by its identity"""
        raise NotImplementedError()
