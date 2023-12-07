from uuid import uuid4
from api.src.application.dto.user_dto import UserDtoInput, UserDtoOutput
from api.src.domain.entities.usuario.usuario import Usuario, Role
from api.src.infra.repository.mongodb_turma_repository import MongodbTurmaRepository
from api.src.infra.repository.mongodb_usuario_repository import MongodbUsuarioRepository
from api.src.domain.exceptions.exceptions import (
    UserNotFoundException,
    TurmaNotFoundException
)

class CreateUserUseCase():
    def __init__(self, usuario_repository: MongodbUsuarioRepository):
        self.usuario_repository = usuario_repository

    def execute(self, user_dto_input: UserDtoInput) -> UserDtoOutput:
        user = Usuario(id=str(uuid4()), discord_id=user_dto_input.discord_id)
        self.usuario_repository.insert(user)
        return UserDtoOutput(id=user.id, discord_id=user.discord_id)


class GrantRoleToUsuario():
    def __init__(self, usuario_repository: MongodbUsuarioRepository):
        self.usuario_repository = usuario_repository

    def execute(self, discord_id: str, rolename: str) -> None:
        user_fetched = self.usuario_repository.get_by_discord_id(discord_id)
        if user_fetched is None:
            raise UserNotFoundException

        user_fetched.grant_role(Role[rolename])
        self.usuario_repository.update(user_fetched)


class RevokeRoleFromUsuario():
    def __init__(self, usuario_repository: MongodbUsuarioRepository):
        self.usuario_repository = usuario_repository

    def execute(self, discord_id: str, rolename: str) -> None:
        user_fetched = self.usuario_repository.get_by_discord_id(discord_id)
        if user_fetched is None:
            raise UserNotFoundException

        user_fetched.revoke_role(Role[rolename])
        self.usuario_repository.update(user_fetched)


class RegistrarAlunoUseCase():
    def __init__(self, usuario_repository: MongodbUsuarioRepository,
                 turma_repo: MongodbTurmaRepository):
        self.usuario_repository = usuario_repository
        self.turma_repo = turma_repo

    def execute(self, turma_id: str, discord_id: str, matricula: str) -> None:
        turma_fetched = self.turma_repo.get_by_id(turma_id)
        if turma_fetched is None:
            raise TurmaNotFoundException

        aluno_id = None
        for aluno in turma_fetched.alunos:
            if matricula == aluno.matricula:
                aluno_id = aluno.id
                break

        if aluno_id is None:
            raise Exception('Matricula nao esta presente na turma')

        user_fetched = self.usuario_repository.get_by_id(aluno_id)

        if user_fetched is None:
            raise UserNotFoundException

        user_fetched.subscribe(discord_id)
        self.usuario_repository.update(user_fetched)


