from abc import abstractmethod
from typing import Optional, List
from ..entities.turma.turma import Turma
from .abstract_repository import AbstractRepository


class AbstractTurmaRepository(AbstractRepository):

    @abstractmethod
    def insert(self, entity: Turma) -> Optional[Turma]:
        pass

    @abstractmethod
    def get_by_id(self, turma_id) -> Optional[Turma]:
        pass

    @abstractmethod
    def update(self, turma: Turma) -> None:
        pass

    @abstractmethod
    def delete(self, turma_id):
        pass

    @abstractmethod
    def list(self) -> List[Turma]:
        pass