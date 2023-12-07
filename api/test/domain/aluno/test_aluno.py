import unittest
from api.src.domain.entities.aluno.aluno import Aluno

class MyTestCase(unittest.TestCase):
    def test_should_create_an_aluno(self):
        aluno = Aluno(id='123', nome='aluno nome', matricula='111222', turma='2A')
        self.assertIsInstance(aluno, Aluno)
        self.assertEqual(aluno.id, '123')
        self.assertEqual(aluno.nome, 'aluno nome')
        self.assertEqual(aluno.matricula, '111222')
        self.assertEqual(aluno.turma, '2A')
        
    def test_should_raise_exception_when_aluno_has_empty_id(self):
        with self.assertRaises(Exception) as ctx:
            Aluno(id='', nome='aluno nome', matricula='111222', turma='2A')
        self.assertEqual(str(ctx.exception), 'Id nao pode ser vazio')

    def test_should_raise_exception_when_aluno_has_empty_nome(self):
        with self.assertRaises(Exception) as ctx:
            Aluno(id='123', nome='', matricula='111222', turma='2A')
        self.assertEqual(str(ctx.exception), 'Nome nao pode ser vazio')

    def test_should_raise_exception_when_aluno_has_empty_matricula(self):
        with self.assertRaises(Exception) as ctx:
            Aluno(id='123', nome='aluno nome', matricula='', turma='2A')
        self.assertEqual(str(ctx.exception), 'Matricula nao pode ser vazio')

    def test_should_raise_exception_when_aluno_has_empty_turma(self):
        with self.assertRaises(Exception) as ctx:
            Aluno(id='123', nome='aluno nome', matricula='111222', turma='')
        self.assertEqual(str(ctx.exception), 'Turma nao pode ser vazio')


if __name__ == '__main__':
    unittest.main()
