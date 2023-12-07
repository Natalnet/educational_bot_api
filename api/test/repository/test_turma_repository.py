import unittest
from datetime import date
from mongomock import MongoClient
from api.src.domain.entities.aluno.aluno import Aluno
from api.src.domain.entities.miniteste.miniteste import Miniteste, Alternativas
from api.src.domain.entities.turma.turma import Turma
from api.src.domain.entities.usuario.usuario import Usuario, Role
from ...src.infra.repository.mongodb_turma_repository import MongodbTurmaRepository


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.mock_client = MongoClient()

    def tearDown(self):
        self.mock_client.close()

    def test_should_session_is_active(self):
        self.db = self.mock_client['test_db']
        self.collection = self.db['test_collection']
        self.collection.insert_one({"name": "Alice"})
        resultado = self.collection.find_one({"name": "Alice"})
        self.assertEqual(resultado["name"], "Alice")

    def test_should_get_by_id_a_turma(self):
        turma_repo = MongodbTurmaRepository(self.mock_client)
        turma = Turma(id='123', denominacao='turma 1', ano=2023, periodo=2, data_inicio=date(2023, 11, 1),
                      data_fim=date(2023, 12, 1))
        turma_repo.insert(turma)
        result = turma_repo.get_by_id('123')
        self.assertIsInstance(result, Turma)

    def test_should_insert_a_turma(self):
        turma_repo = MongodbTurmaRepository(self.mock_client)
        aluno1 = Aluno(id='123', nome='Joao', matricula='111222', turma='2A')
        aluno2 = Aluno(id='124', nome='Maria', matricula='111223', turma='1B')
        aluno1.registrar_presenca(date.today())
        alunos = [aluno1, aluno2]
        turma = Turma(id='123', denominacao='turma 1', ano=2023, periodo=2, data_inicio=date(2023, 11, 1),
                      data_fim=date(2023, 12, 1))
        turma.add_alunos(alunos)

        docente = Usuario(id='125', discord_id='112233')
        docente.grant_role(Role.DOCENTE)
        turma.definir_docente(docente)

        miniteste1 = Miniteste(id='321', teste_id='T01', pergunta='quanto e dois mais dois?',
                             resposta='B', alternativas=Alternativas(A='2', B='4', C='5', D='0'))
        turma.add_miniteste([miniteste1])
        turma_repo.insert(turma)

    def test_should_update_a_turma(self):
        turma_repo = MongodbTurmaRepository(self.mock_client)
        turma = Turma(id='123', denominacao='turma 1', ano=2023, periodo=2, data_inicio=date(2023, 11, 1),
                      data_fim=date(2023, 12, 1))
        turma_repo.insert(turma)
        result = turma_repo.get_by_id('123')
        self.assertEqual(result.ano, 2023)
        turma.ano = 2024
        turma_repo.update(turma)
        result = turma_repo.get_by_id('123')
        self.assertEqual(result.ano, 2024)


if __name__ == '__main__':
    unittest.main()
