import unittest
from datetime import date
from api.src.domain.entities.turma.turma import Turma
from api.src.domain.entities.aluno.aluno import Aluno
from api.src.domain.entities.usuario.usuario import Usuario, Role
from api.src.domain.entities.miniteste.miniteste import Miniteste, Alternativas

class TurmaTestCase(unittest.TestCase):
    def test_should_create_a_turma(self):
        turma = Turma(id='123', denominacao='turma 1', ano=2023, periodo=2, data_inicio=date(2023, 11, 1),
                      data_fim=date(2023, 12, 1))
        self.assertIsInstance(turma, Turma)
        self.assertEqual(turma.id, '123')
        self.assertEqual(turma.denominacao, 'turma 1')
        self.assertEqual(turma.ano, 2023)
        self.assertEqual(turma.periodo, 2)
        self.assertEqual(turma.data_inicio, date(2023, 11, 1))
        self.assertEqual(turma.data_fim, date(2023, 12, 1))
        self.assertFalse(turma.esta_consolidada)

    def test_should_raise_exception_if_id_invalida(self):
        with self.assertRaises(Exception) as ctx:
            Turma(id='', denominacao='', ano=2023, periodo=2, data_inicio=date(2023, 11, 1),
                  data_fim=date(2023, 12, 1))
        self.assertEqual(str(ctx.exception), 'Id nao pode ser vazio')

    def test_should_raise_exception_if_denominacao_invalida(self):
        with self.assertRaises(Exception) as ctx:
            Turma(id='123', denominacao='', ano=2023, periodo=2, data_inicio=date(2023, 11, 1),
                  data_fim=date(2023, 12, 1))
        self.assertEqual(str(ctx.exception), 'Denominacao nao permitida')

    def test_should_raise_exception_if_data_fim_antes_de_data_inicio(self):
        with self.assertRaises(Exception) as ctx:
            Turma(id='123', denominacao='turma 1', ano=2023, periodo=2, data_inicio=date(2023, 12, 1),
                  data_fim=date(2023, 11, 1))
        self.assertEqual(str(ctx.exception), 'Data fim deve ser apos a Data inicio da turma')

    def test_should_consolidar_turma(self):
        turma = Turma(id='123', denominacao='turma 1', ano=2023, periodo=2, data_inicio=date(2023, 11, 1),
                      data_fim=date(2023, 12, 1))
        self.assertFalse(turma.esta_consolidada)
        turma.consolidar()
        self.assertTrue(turma.esta_consolidada)

    def test_should_add_aluno_to_turma(self):
        aluno1 = Aluno(id='123', nome='Joao', matricula='111222', turma='2A')
        aluno2 = Aluno(id='124', nome='Maria', matricula='111223', turma='1B')
        alunos = [aluno1, aluno2]
        turma = Turma(id='123', denominacao='turma 1', ano=2023, periodo=2, data_inicio=date(2023, 11, 1),
                      data_fim=date(2023, 12, 1))
        self.assertEqual(turma.alunos, [])
        turma.add_alunos(alunos)
        self.assertEqual(len(turma.alunos), 2)
        self.assertEqual(turma.alunos, [aluno1, aluno2])

    def test_should_add_minitest_to_turma(self):
        alternativas1 = Alternativas(A='alternativa A', B='alternativa B', C='alternativa C', D='alternativa D')
        miniteste1 = Miniteste(id='123', teste_id='T01', pergunta='pergunta?', resposta='A', alternativas=alternativas1)
        alternativas2 = Alternativas(A='alternativa A', B='alternativa B', C='alternativa C', D='alternativa D')
        miniteste2 = Miniteste(id='124', teste_id='T02', pergunta='pergunta?', resposta='B', alternativas=alternativas2)
        minitestes = [miniteste1, miniteste2]
        turma = Turma(id='123', denominacao='turma 1', ano=2023, periodo=2, data_inicio=date(2023, 11, 1),
                      data_fim=date(2023, 12, 1))
        self.assertEqual(turma.minitestes, [])
        turma.add_miniteste(minitestes)
        self.assertEqual(len(turma.minitestes), 2)
        self.assertEqual(turma.minitestes, [miniteste1, miniteste2])

    def test_should_definir_monitor(self):
        turma = Turma(id='123', denominacao='turma 1', ano=2023, periodo=2, data_inicio=date(2023, 11, 1),
                      data_fim=date(2023, 12, 1))
        monitor = Usuario(id='123', discord_id='112233')
        monitor.grant_role(Role.MONITOR)
        turma.add_monitor(monitor)
        self.assertEqual(len(turma.monitores), 1)

    def test_should_raise_exception_when_add_monitor_and_user_is_not_monitor(self):
        with self.assertRaises(Exception) as ctx:
            turma = Turma(id='123', denominacao='turma 1', ano=2023, periodo=2, data_inicio=date(2023, 11, 1),
                          data_fim=date(2023, 12, 1))
            monitor = Usuario(id='123', discord_id='112233')
            monitor.grant_role(Role.DISCENTE)
            turma.add_monitor(monitor)
        self.assertEqual(len(turma.monitores), 0)
        self.assertEqual(str(ctx.exception), f'O usuario nao possui a role {Role.MONITOR}')

    def test_should_definir_docente(self):
        turma = Turma(id='123', denominacao='turma 1', ano=2023, periodo=2, data_inicio=date(2023, 11, 1),
                      data_fim=date(2023, 12, 1))
        docente = Usuario(id='123', discord_id='112233')
        docente.grant_role(Role.DOCENTE)
        self.assertIsNone(turma.docente)
        turma.definir_docente(docente)
        self.assertIsNotNone(turma.docente)
        self.assertIsInstance(turma.docente, Usuario)

    def test_should_raise_exception_when_definir_docente_and_user_is_not_docente(self):
        with self.assertRaises(Exception) as ctx:
            turma = Turma(id='123', denominacao='turma 1', ano=2023, periodo=2, data_inicio=date(2023, 11, 1),
                          data_fim=date(2023, 12, 1))
            docente = Usuario(id='123', discord_id='112233')
            docente.grant_role(Role.DISCENTE)
            turma.definir_docente(docente)
        self.assertIsNone(turma.docente)
        self.assertEqual(str(ctx.exception), f'O usuario nao possui a role {Role.DOCENTE}')


if __name__ == '__main__':
    unittest.main()
