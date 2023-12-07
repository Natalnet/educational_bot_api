from pydantic import BaseModel


class PresencaAlunoDto(BaseModel):
    nome: str
    matricula: str
    frequencia: list
