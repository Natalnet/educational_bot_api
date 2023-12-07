from abc import abstractmethod
from typing import Optional, List
from .abstract_repository import AbstractRepository
from ..entities.usuario.usuario import Usuario


class AbstractUsuarioRepository(AbstractRepository):

    @abstractmethod
    def insert(self, user: Usuario) -> Optional[Usuario]:
        pass

    @abstractmethod
    def get_by_id(self, user_id: str) -> Optional[Usuario]:
        pass

    @abstractmethod
    def get_by_discord_id(self, user_discord_id: str) -> Optional[Usuario]:
        pass

    @abstractmethod
    def update(self, user: Usuario) -> None:
        pass

    @abstractmethod
    def list(self) -> List[Usuario]:
        pass