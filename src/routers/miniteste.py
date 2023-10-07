from fastapi import APIRouter, HTTPException, status
from src.services.miniteste_service import MinitesteService
from src.models.miniteste import Miniteste, MinitesteAluno
from src.exceptions import TurmaNotFound

miniteste_service = MinitesteService()

router = APIRouter(prefix='/minitestes', tags=['miniteste'])

@router.get("/random/turmas/{turma_id}", status_code=200)
async def buscar_aleatorio(turma_id: str):
    try:
        return miniteste_service.buscar(turma_id) 
    except TurmaNotFound as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Turma não encontrada') from exc
    
@router.post("/turmas/{turma_id}", status_code=200)
async def responder(turma_id: str, miniteste_aluno: MinitesteAluno):
    try:
        res = miniteste_service.responder(turma_id, miniteste_aluno)
        return {'response': 'Correto' if res else 'Errado'}
    except TurmaNotFound as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Turma não encontrada') from exc

@router.get("/{teste_id}/turmas/{turma_id}", status_code=200)
async def responder(teste_id: str, turma_id: str):
    try:
        res = miniteste_service.status(turma_id, teste_id)
        return res
    except TurmaNotFound as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail='Turma não encontrada') from exc