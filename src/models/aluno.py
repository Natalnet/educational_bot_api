from typing import List
from pydantic import BaseModel

class Aluno(BaseModel):
    matricula: str
    discord_id: str | None

    def validate(self):
        return True

    def to_dict(self):
        return {
            'matricula': self.matricula,
            'discord_id': self.discord_id
        }

class AlunoTurma(BaseModel):
    nome: str
    matricula: str
    turma: str

class AlunoTurmaList(BaseModel):
    data: List[AlunoTurma]