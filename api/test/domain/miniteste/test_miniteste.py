import unittest
from ....src.domain.entities.miniteste.miniteste import Miniteste, Alternativas


class MyTestCase(unittest.TestCase):
    def test_should_create_a_miniteste(self):
        alternativas = Alternativas(A='alternativa A', B='alternativa B', C='alternativa C', D='alternativa D')
        miniteste = Miniteste(id='123', teste_id='T01', pergunta='pergunta?', resposta='A', alternativas=alternativas)
        self.assertIsInstance(miniteste, Miniteste)
        self.assertEqual(miniteste.id, '123')
        self.assertEqual(miniteste.teste_id, 'T01')
        self.assertEqual(miniteste.pergunta, 'pergunta?')
        self.assertEqual(miniteste.resposta, 'A')
        self.assertEqual(miniteste.alternativas, alternativas)

    def test_should_raise_exception_when_id_is_empty(self):
        with self.assertRaises(Exception) as ctx:
            alternativas = Alternativas(A='alternativa A', B='alternativa B', C='alternativa C', D='alternativa D')
            Miniteste(id='', teste_id='T01', pergunta='pergunta?', resposta='A',
                      alternativas=alternativas)
        self.assertEqual(str(ctx.exception), 'Id nao pode ser vazio')

    def test_should_raise_exception_when_teste_id_is_empty(self):
        with self.assertRaises(Exception) as ctx:
            alternativas = Alternativas(A='alternativa A', B='alternativa B', C='alternativa C', D='alternativa D')
            Miniteste(id='123', teste_id='', pergunta='pergunta?', resposta='A',
                      alternativas=alternativas)
        self.assertEqual(str(ctx.exception), 'Teste Id nao pode ser vazio')

    def test_should_raise_exception_when_pergunta_is_empty(self):
        with self.assertRaises(Exception) as ctx:
            alternativas = Alternativas(A='alternativa A', B='alternativa B', C='alternativa C', D='alternativa D')
            Miniteste(id='123', teste_id='T01', pergunta='', resposta='A',
                      alternativas=alternativas)
        self.assertEqual(str(ctx.exception), 'Pergunta nao pode ser vazio')

    def test_should_raise_exception_when_resposta_is_empty(self):
        with self.assertRaises(Exception) as ctx:
            alternativas = Alternativas(A='alternativa A', B='alternativa B', C='alternativa C', D='alternativa D')
            Miniteste(id='123', teste_id='T01', pergunta='pergunta?', resposta='',
                      alternativas=alternativas)
        self.assertEqual(str(ctx.exception), 'Resposta nao pode ser vazio')


if __name__ == '__main__':
    unittest.main()
