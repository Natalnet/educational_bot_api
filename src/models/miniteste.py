from pydantic import BaseModel

class Miniteste(BaseModel):
    teste_id: str
    pergunta: str
    alternativas: object
    resposta: str

class MinitesteAluno(BaseModel):
    teste_id: str
    aluno_id: str
    resposta: str