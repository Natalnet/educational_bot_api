from uuid import uuid4
from src.data.mongodb import connection
from src.models.miniteste import Miniteste, MinitesteAluno
from src.services.turma_service import TurmaService
from src.services.aluno_service import AlunoService

class MinitesteService():
    
    def __init__(self):
        client = connection
        db = client.apibotdb
        self.collection = db.miniteste
        self.turma_service = TurmaService()
        self.aluno_service = AlunoService()
    
    def buscar(self, turma_id: str):
        return self.turma_service.buscar_miniteste_random(turma_id)

    def responder(self, turma_id: str, miniteste_aluno: MinitesteAluno):

        teste_id = miniteste_aluno.teste_id
        
        miniteste = self.turma_service.buscar_miniteste_por_id(turma_id, teste_id)

        if miniteste_aluno.resposta == miniteste['resposta']:
            self.collection.insert_one({
                '_id': str(uuid4()),
                'miniteste_id': miniteste_aluno.teste_id,
                'aluno_id': miniteste_aluno.aluno_id,
                'resposta': miniteste_aluno.resposta,
                'resultado': True
            })
            self.turma_service.atualizar_miniteste_acertos_e_total(turma_id, miniteste_aluno.teste_id)
            return True
        self.collection.insert_one({
            '_id': str(uuid4()),
            'miniteste_id': miniteste_aluno.teste_id,
            'aluno_id': miniteste_aluno.aluno_id,
            'resposta': miniteste_aluno.resposta,
            'resultado': False
        })
        self.turma_service.atualizar_miniteste_total(turma_id, miniteste_aluno.teste_id)
        return False
    
    def status(self, turma_id: str, teste_id: str):

        miniteste = self.turma_service.buscar_miniteste_por_id(turma_id, teste_id)

        taxa_acerto = miniteste['total_acertos']/miniteste['total_respostas']

        return {
            'turma_id': turma_id,
            'teste_id': teste_id,
            'total_respostas': miniteste['total_respostas'],
            'taxa_acerto': f'{taxa_acerto:.2%}'
        }

