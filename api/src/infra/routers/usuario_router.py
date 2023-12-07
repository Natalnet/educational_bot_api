from fastapi import APIRouter, HTTPException, status
from api.src.infra.database.mongomock_instance import client
from api.src.infra.database.mongodb_instance import connection
from api.src.application.dto.user_dto import UserDtoInput, RegisterDtoInput
from api.src.domain.exceptions.exceptions import UserNotFoundException
from api.src.infra.repository.mongodb_turma_repository import MongodbTurmaRepository
from api.src.infra.repository.mongodb_usuario_repository import MongodbUsuarioRepository
from api.src.application.use_cases.usuario_usecases import (
    CreateUserUseCase,
    GrantRoleToUsuario,
    RevokeRoleFromUsuario,
    RegistrarAlunoUseCase
)

router = APIRouter(prefix='/user', tags=['user'])

usuario_repository = MongodbUsuarioRepository(connection)
turma_reposity = MongodbTurmaRepository(connection)


@router.post("/", status_code=201)
async def criar(user_dto_input: UserDtoInput):
    usecase = CreateUserUseCase(usuario_repository)
    user_dto_output = usecase.execute(user_dto_input)
    return user_dto_output


@router.post("/register/{turma_id}", status_code=201)
async def registrar(turma_id: str, register_dto_input: RegisterDtoInput):
    try:
        usecase = RegistrarAlunoUseCase(usuario_repository, turma_reposity)
        usecase.execute(turma_id, register_dto_input.discord_id, register_dto_input.matricula)
        return {'response': f'Usuario {register_dto_input.discord_id} foi registrado'}
    except UserNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/grant/{discord_id}/{role}", status_code=200)
async def grant_role(discord_id: str, role: str):
    try:
        usercase = GrantRoleToUsuario(usuario_repository)
        usercase.execute(discord_id, role)
        return {'response': f'User {discord_id} role updated'}
    except UserNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Role nao encontrada')


@router.put("/revoke/{discord_id}/{role}", status_code=200)
async def revoke_role(discord_id: str, role: str):
    try:
        usercase = RevokeRoleFromUsuario(usuario_repository)
        usercase.execute(discord_id, role)
        return {'response': f'User {discord_id} role updated'}
    except UserNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Role nao encontrada')