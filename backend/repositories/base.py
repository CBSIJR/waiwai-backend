from abc import abstractmethod, ABCMeta
from sqlalchemy.orm import DeclarativeBase
from typing import List


class Repository(metaclass=ABCMeta):
    """An interface to listing repository"""

    @abstractmethod
    async def create(self, **kwargs) -> None:
        """Adds new entity to a repository"""
        raise NotImplementedError()

    @abstractmethod
    async def get_list(self, **kwargs) -> List[DeclarativeBase]:
        """Removes existing entity from a repository"""
        raise NotImplementedError()

    @abstractmethod
    async def get_by_id(self, **kwargs) -> DeclarativeBase:
        """Retrieves entity by its identity"""
        raise NotImplementedError()

    @abstractmethod
    async def update_by_id(self, **kwargs) -> None:
        """Retrieves entity by its identity"""
        raise NotImplementedError()

    @abstractmethod
    async def delete_by_id(self, **kwargs) -> None:
        """Retrieves entity by its identity"""
        raise NotImplementedError()
