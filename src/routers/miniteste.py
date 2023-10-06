from fastapi import APIRouter, HTTPException, status
from src.services.miniteste_service import Miniteste
from src.models.miniteste import Miniteste

miniteste_service = Miniteste()

router = APIRouter(prefix='/miniteste', tags=['miniteste'])
