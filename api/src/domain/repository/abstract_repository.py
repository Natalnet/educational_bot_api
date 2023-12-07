from abc import ABC, abstractmethod
from typing import Optional, TypeVar, Sequence

T = TypeVar('T')


class AbstractRepository(ABC):
    @abstractmethod
    def insert(self, entity: T) -> Optional[T]:
        pass

    @abstractmethod
    def update(self, entity: T) -> None:
        pass

    @abstractmethod
    def get_by_id(self, id) -> Optional[T]:
        pass

    @abstractmethod
    def delete(self, id) -> None:
        pass

    @abstractmethod
    def list(self) -> Optional[Sequence[T]]:
        pass