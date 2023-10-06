from uuid import uuid4
from typing import List
from src.data.mongodb import connection
from src.models.turma import Turma
from src.models.aluno import Aluno, AlunoTurmaList
from src.models.miniteste import Miniteste
from src.services.admin_service import AdminService
from src.services.aluno_service import AlunoService
from src.exceptions import TurmaAlreadyExists, TurmaNotFound

class TurmaService():
    
    def __init__(self):
        client = connection
        db = client.apibotdb
        self.collection = db.turmas
        self.admin_service = AdminService()
        self.aluno_service = AlunoService()

    def criar(self, turma: Turma):
        filter = {'denominacao': turma.denominacao }
        a_turma = self.collection.find_one(filter)

        if a_turma is not None:
            return TurmaAlreadyExists

        # TODO: check if turma.docente exists and his roles contains 'PROFESSOR'

        id = str(uuid4())

        self.collection.insert_one({
            '_id': id ,
            'denominacao': turma.denominacao,
            'ano': turma.ano,
            'periodo': turma.periodo,
            'esta_consolidada': False,
            'data_inicio': turma.data_inicio,
            'data_fim': turma.data_fim,
            'docente': turma.docente,
            'monitores': [],
            'alunos': turma.alunos,
            'minitestes': []
        })

        print(turma.alunos)

        for aluno in turma.alunos:
            matr = aluno['matricula']
            aluno_buscado = self.aluno_service.buscar_por_matricula(matr)
            if aluno_buscado is None:
                an_aluno = Aluno(matricula=matr, discord_id=None)
                self.aluno_service.register(aluno=an_aluno)
                self.aluno_service.colocar_em_turma(matricula=matr, turma_id=id)
            else:
                self.aluno_service.colocar_em_turma(matricula=matr, turma_id=id)

    def buscar_por_id(self, turma_id: str):
        filter = {'_id': turma_id }
        return self.collection.find_one(filter)
    
    def adicionar_alunos(self, turma_id: str, alunos_turma: AlunoTurmaList):
        filter = {'_id': turma_id }
        a_turma = self.collection.find_one(filter)

        if a_turma is None:
            return TurmaNotFound

        turma_alunos = a_turma['alunos']
        for aluno in alunos_turma:
            turma_alunos.append(aluno)

        turma_updated = { '$set': {
            'alunos': turma_alunos,
        }}
        self.collection.update_one(filter, turma_updated)

    def adicionar_monitor(self, turma_id: str, monitor_id: str):
        filter = {'_id': turma_id }
        a_turma = self.collection.find_one(filter)

        if a_turma is None:
            return TurmaNotFound

        # obter usuário por id e checar se possui role monitor
        an_user = self.admin_service.buscar(monitor_id)

        if an_user is None:
            return Exception

        user_roles = an_user['roles']
        turma_monitores = a_turma['monitores']
        if 'MONITOR' in user_roles:
            turma_monitores.append(an_user['_id'])
    
    def adicionar_minitestes(self, turma_id: str, minitestes: List[Miniteste]) -> None:
        filter_id = {'_id': turma_id }
        a_turma = self.collection.find_one(filter_id)

        if a_turma is None:
            return TurmaNotFound

        turma_minitestes = a_turma['minitestes']
        for miniteste in minitestes:
            turma_minitestes.append(miniteste)

        turma_updated = { '$set': {
            'minitestes': [a_turma['minitestes']],
        }}
        self.collection.update_one(filter_id, turma_updated)
        return None

    def consolidar(self, turma_id: str):
        a_turma = self.buscar_por_id(turma_id=turma_id)

        if a_turma is None:
            return TurmaNotFound

        turma_updated = { '$set': {
            'esta_consolidada': True,
        }}
        self.collection.update_one({'_id': turma_id }, turma_updated)

    def reabrir(self, turma_id: str):
        # reabrir uma turma
        pass

    def obter_frequencia(self, turma_id: str):
        a_turma = self.buscar_por_id(turma_id=turma_id)

        if a_turma is None:
            return TurmaNotFound

        freq_turma = []

        alunos_turma = a_turma['alunos']

        for aluno in alunos_turma:
            matr = aluno['matricula']
            aluno_buscado = self.aluno_service.buscar_por_matricula(matr)
            freq_aluno = self.aluno_service.obter_presenca(aluno_buscado['_id'], turma_id)
            freq_turma.append(freq_aluno)
        
        return freq_turma