from typing import List
from api.src.infra.database.mongomock_instance import client
from api.src.infra.database.mongodb_instance import connection
from fastapi import APIRouter, HTTPException, status
from api.src.application.dto.turma_dto_input import TurmaDtoInput, AlunoDto
from api.src.application.dto.miniteste_dto import MinitestesDto, ResponderMinitesteDto
from api.src.infra.repository.mongodb_turma_repository import MongodbTurmaRepository
from api.src.infra.repository.mongodb_usuario_repository import MongodbUsuarioRepository
from api.src.application.use_cases.turma_usecases import (
    CadastrarTurmaUseCase,
    CadastrarAlunoEmTurmaUseCase,
    AddMinitesteToTurma,
    AddDocenteToTurmaUseCase,
    AddMonitorToTurmaUseCase,
    RegistrarPresencaUseCase,
    ResponderMinitesteUseCase,
    ObterFrequenciaTurmaUseCase
)
from api.src.domain.exceptions.exceptions import (
    TurmaNotFoundException,
    UserNotFoundException,
    InvalidDateRegistrarPresencaException)

router = APIRouter(prefix='/turmas', tags=['turma'])

turma_reposity = MongodbTurmaRepository(connection)
usuario_repository = MongodbUsuarioRepository(connection)


@router.post("/", status_code=201)
async def cadastrar_turma(turma_dto_input: TurmaDtoInput):
    try:
        usecase = CadastrarTurmaUseCase(turma_reposity, usuario_repository)
        turma_dto_output = usecase.execute(turma_dto_input)
        return {
            'response': 'Turma foi cadastrada com sucesso',
            'turma_id': turma_dto_output.id,
            'denominacao': turma_dto_output.denominacao
        }
    except Exception:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='Error')


@router.post("/{turma_id}/alunos", status_code=200)
async def adicionar_alunos(turma_id: str, alunos: List[AlunoDto]):
    try:
        usecase = CadastrarAlunoEmTurmaUseCase(turma_reposity, usuario_repository)
        usecase.execute(turma_id, alunos)
        return {'response': 'Os alunos foram cadastrados com sucesso na turma'}
    except TurmaNotFoundException as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{turma_id}/docente/{discord_id}", status_code=200)
async def definir_docente(turma_id: str, discord_id: str):
    try:
        usecase = AddDocenteToTurmaUseCase(turma_reposity, usuario_repository)
        usecase.execute(turma_id, discord_id)
        return {'response': 'O docente foi definido como professor da turma'}
    except TurmaNotFoundException as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))
    except UserNotFoundException as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/{turma_id}/monitor/{discord_id}", status_code=200)
async def adicionar_monitor(turma_id: str, discord_id: str):
    try:
        usecase = AddMonitorToTurmaUseCase(turma_reposity, usuario_repository)
        usecase.execute(turma_id, discord_id)
        return {'response': 'O monitor foi adicionado a turma'}
    except TurmaNotFoundException as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))
    except UserNotFoundException as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/{turma_id}/minitestes", status_code=200)
async def adicionar_minitestes(turma_id: str, minitestes: List[MinitestesDto]):
    try:
        usecase = AddMinitesteToTurma(turma_reposity)
        usecase.execute(turma_id, minitestes)
        return {'response': 'Os minitestes foram adicionados com sucesso na turma'}
    except TurmaNotFoundException as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/{turma_id}/user/{discord_id}/presenca", status_code=200)
async def registrar_presenca(turma_id: str, discord_id: str):
    try:
        usecase = RegistrarPresencaUseCase(turma_reposity, usuario_repository)
        usecase.execute(turma_id, discord_id)
        return {'response': 'Presença registrada com sucesso'}
    except TurmaNotFoundException as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))
    except UserNotFoundException as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))
    except InvalidDateRegistrarPresencaException as e:
        raise HTTPException(status.HTTP_409_CONFLICT, detail=str(e))


@router.post("/{turma_id}/user/{discord_id}/miniteste", status_code=200)
async def responder_miniteste(turma_id: str, discord_id: str, resposta_miniteste_dto: ResponderMinitesteDto):
    try:
        usecase = ResponderMinitesteUseCase(turma_reposity, usuario_repository)
        result = usecase.execute(turma_id, discord_id, resposta_miniteste_dto)
        return {'response': result}
    except TurmaNotFoundException as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))
    except UserNotFoundException as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/{turma_id}/presenca", status_code=200)
async def obter_presenca_turma(turma_id: str):
    try:
        usecase = ObterFrequenciaTurmaUseCase(turma_reposity)
        result = usecase.execute(turma_id)
        return result
    except TurmaNotFoundException as e:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=str(e))