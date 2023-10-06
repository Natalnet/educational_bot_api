from uuid import uuid4
from src.data.mongodb import connection
from src.models.miniteste import Miniteste

class MinitesteService():
    
    def __init__(self):
        pass

    def adicionar(self, turma_id: str):
        # adiciona miniteste em turma
        pass

    def responder(self, id: str, turma_id: str, aluno_id: str):
        # aluno responde miniteste da uma turma
        pass
