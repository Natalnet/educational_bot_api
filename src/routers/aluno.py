from fastapi import APIRouter, HTTPException, status
from src.services.aluno_service import AlunoService
from src.models.aluno import Aluno

aluno_service = AlunoService()

router = APIRouter(prefix='/alunos', tags=['aluno'])

@router.post("/", status_code=201)
async def registrar(aluno: Aluno):
    try:
        status = aluno_service.register(aluno=aluno)
        return {'response' : f'Aluno {status} sucessfully'}
    except Exception:
        return {'err': 'some error'}

@router.put("/{aluno_id}/turmas/{turma_id}", status_code=200)
async def adicionar_em_turma(aluno_id: str, turma_id: str):
    aluno_service.colocar_em_turma(aluno_id, turma_id)

@router.post("/{aluno_id}/turmas/{turma_id}", status_code=200)
async def registrar_presenca(aluno_id: str, turma_id: str):
    aluno_service.registrar_presenca(aluno_id=aluno_id, turma_id=turma_id)

@router.get("/{aluno_id}/turmas/{turma_id}", status_code=200)
async def obter_presenca(aluno_id: str, turma_id: str):
    freq = aluno_service.obter_presenca(aluno_id=aluno_id, turma_id=turma_id)
    return {'freq':freq}