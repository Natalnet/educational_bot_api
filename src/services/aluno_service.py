from uuid import uuid4
import datetime
from src.data.mongodb import connection
from src.models.aluno import Aluno

class AlunoService():
    
    def __init__(self):
        client = connection
        db = client.apibotdb
        self.collection = db.alunos

    def register(self, aluno: Aluno):
        # if not aluno.validate():
        #     return Exception

        filter = {'matricula': aluno.matricula }
        an_aluno = self.collection.find_one(filter)

        print(an_aluno)

        if an_aluno is None:
            self.collection.insert_one({
                '_id': str(uuid4()),
                'discord_id': aluno.discord_id,
                'matricula': aluno.matricula,
                'turmas': [],
                'created_at': str(datetime.datetime.now()),
                'updated_at': str(datetime.datetime.now())
            })
            return 'registered'
        aluno_updated = { '$set': {
            'discord_id': aluno.discord_id,
            'updated_at': str(datetime.datetime.now())
        }}
        self.collection.update_one(filter, aluno_updated)
        return 'updated'
    
    def buscar_por_matricula(self, matricula: str):
        filter = {'matricula': matricula }
        return self.collection.find_one(filter)
    
    def detalhar(self, id: str, aluno: Aluno):
        # Nome
        # created at
        # turmas
        # frequencia
        pass

    def colocar_em_turma(self, matricula: str, turma_id: str):
        filter = {'matricula': matricula }
        an_aluno = self.collection.find_one(filter)

        if an_aluno is None:
            return Exception
        
        turma = {'turma_id': turma_id, 'freq': 0, 'datas_registradas': []}
        aluno_turmas = an_aluno['turmas']
        aluno_turmas.append(turma)

        aluno_updated = { '$set': {
            'turmas': aluno_turmas,
            'updated_at': str(datetime.datetime.now())
        }}
        self.collection.update_one(filter, aluno_updated)
    
    def registrar_presenca(self, aluno_id: str, turma_id: str):
        filter = {'_id': aluno_id }
        an_aluno = self.collection.find_one(filter)

        if an_aluno is None:
            return Exception
        
        aluno_turmas = an_aluno['turmas']

        for turma in aluno_turmas:
            if turma['turma_id'] == turma_id:
                alunos_datas_registradas = turma['datas_registradas']

                # O aluno já registrou presença hoje
                if datetime.date.today() in alunos_datas_registradas:
                    return

                turma['freq'] = turma['freq'] + 2
                alunos_datas_registradas.append(str(datetime.date.today()))
                aluno_updated = { '$set': {
                    'turmas': aluno_turmas,
                }}
                self.collection.update_one(filter, aluno_updated)
                break
            
        # return TurmaNotFound
    
    def obter_presenca(self, aluno_id: str, turma_id: str):
        filter = {'_id': aluno_id }
        an_aluno = self.collection.find_one(filter)

        if an_aluno is None:
            return Exception
        
        aluno_turmas = an_aluno['turmas']

        for turma in aluno_turmas:
            if turma['turma_id'] == turma_id:
                return turma['freq']
                break
        
        # return TurmaNotFound