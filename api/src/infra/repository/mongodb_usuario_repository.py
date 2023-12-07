from typing import Optional

from ...domain.repository.abstract_usuario_repository import AbstractUsuarioRepository
from ....src.domain.entities.usuario.usuario import Usuario


class MongodbUsuarioRepository(AbstractUsuarioRepository):

    def __init__(self, client):
        self.client = client
        self.db = client.apibotv2
        self.collection = self.db.usuarios

    def insert(self, user: Usuario) -> Optional[Usuario]:
        user_dict = user.to_dict()
        self.collection.insert_one(user_dict)

    def get_by_id(self, user_id: str) -> Optional[Usuario]:
        result = self.collection.find_one({'_id': user_id})
        if result is None:
            return None
        else:
            return Usuario.from_dic(result)

    def get_by_discord_id(self, user_discord_id: str) -> Optional[Usuario]:
        result = self.collection.find_one({'discord_id': user_discord_id})
        if result is None:
            return None
        else:
            return Usuario.from_dic(result)

    def update(self, user: Usuario):
        self.collection.update_one({"_id": user.id}, {"$set": user.to_dict()})

    def list(self):
        users = self.collection.find()
        return [Usuario.from_dic(user) for user in users]

    def delete(self, user_id) -> None:
        pass


