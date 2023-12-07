from typing import Optional, List
from api.src.domain.entities.turma.turma import Turma
from ...domain.repository.abstract_turma_repository import AbstractTurmaRepository
from .mongodb_usuario_repository import MongodbUsuarioRepository


class MongodbTurmaRepository(AbstractTurmaRepository):

    def __init__(self, client):
        self.client = client
        self.db = client.apibotv2
        self.collection = self.db.turmas
        self.usuario_repository = MongodbUsuarioRepository(client)

    def insert(self, turma: Turma) -> Optional[Turma]:
        turma_dict = turma.to_dict()
        self.collection.insert_one(turma_dict)

    def get_by_id(self, turma_id) -> Optional[Turma]:
        turma_opt = self.collection.find_one({'_id': turma_id})
        if turma_opt is None:
            return None
        turma = Turma.from_dict(turma_opt)
        if turma_opt['docente']:
            docente = self.usuario_repository.get_by_id(turma_opt['docente'])
            turma.definir_docente(docente)
        for id in turma_opt.get('monitores', []):
            monitor = self.usuario_repository.get_by_id(id)
            turma.add_monitor(monitor)
        return turma

    def update(self, turma: Turma) -> None:
        self.collection.update_one({"_id": turma.id}, {"$set": turma.to_dict()})

    def delete(self, turma_id) -> None:
        pass

    def list(self) -> List[Turma]:
        pass
