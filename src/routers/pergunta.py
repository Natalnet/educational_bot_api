from fastapi import APIRouter, HTTPException, status
from src.services.pergunta_service import PerguntaService
from src.models.pergunta import Pergunta

pergunta_service = PerguntaService()

router = APIRouter(prefix='/perguntas', tags=['perguntas'])

@router.post("/", status_code=201)
async def adicionar(pergunta: Pergunta):
    try:
        pergunta_service.adicionar(pergunta=pergunta)
        return {'response': 'Pergunta registrada com sucesso'}
    except Exception:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail='Missing information')
