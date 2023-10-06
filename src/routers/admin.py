from fastapi import APIRouter, HTTPException, status
from src.exceptions import *
from src.models.usuario import Usuario
from src.services.admin_service import AdminService

admin_service = AdminService()

router = APIRouter(prefix='/admin', tags=['admin'])

@router.post("/", status_code=201)
async def registrar(usuario: Usuario):
    admin_service.registrar(usuario=usuario)

@router.put("/grant/{discord_id}/{role}", status_code=200)
async def grant_role(discord_id: str, role: str):
    try:
        admin_service.grant_role(discord_id=discord_id, role=role)
        return {'response': f'User {discord_id} role updated'}
    except UserNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')

@router.put("/revoke/{discord_id}/{role}", status_code=200)
async def revoke_role(discord_id: str, role: str):
    try:
        admin_service.revoke_role(discord_id=discord_id, role=role)
        return {'response': f'User {discord_id} role updated'}
    except UserNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='User not found')