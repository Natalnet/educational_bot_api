from typing import List
from pydantic import BaseModel


class AlunoDto(BaseModel):
    nome: str
    matricula: str
    turma: str


class TurmaDtoInput(BaseModel):
    denominacao: str
    ano: int
    periodo: int
    data_inicio: str
    data_fim: str
    alunos: List[AlunoDto]
