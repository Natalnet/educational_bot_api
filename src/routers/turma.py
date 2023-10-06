from typing import List
from fastapi import APIRouter, HTTPException, status
from src.services.turma_service import TurmaService
from src.models.turma import Turma
from src.models.aluno import AlunoTurma
from src.models.miniteste import Miniteste
from src.exceptions import TurmaAlreadyExists, TurmaNotFound

turma_service = TurmaService()

router = APIRouter(prefix='/turmas', tags=['turma'])

@router.post("/", status_code=201)
async def cadastrar_turma(turma: Turma):
    try:
        turma_service.criar(turma=turma)
        return {'response': 'Turma foi cadastrada com sucesso.'}
    except TurmaAlreadyExists as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, detail='Turma com denominação já existe') from exc

@router.post("/{turma_id}/alunos", status_code=200)
async def adicionar_alunos(turma_id: str, alunos: List[AlunoTurma]):
    try:
        alunos_turma_dict = [aluno.dict() for aluno in alunos]
        turma_service.adicionar_alunos(turma_id, alunos_turma_dict)
        return {'response': 'O alunos foram cadastrados com sucesso na turma'}
    except TurmaNotFound as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Turma não com encontrada') from exc

@router.post("/{turma_id}/minitestes", status_code=200)
async def adicionar_minitestes(turma_id: str, minitestes: List[Miniteste]):
    try:
        minitestes_turma_dict = [minitestes.dict() for miniteste in minitestes]
        turma_service.adicionar_minitestes(turma_id, minitestes_turma_dict)
    except TurmaNotFound as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Turma não com encontrada') from exc