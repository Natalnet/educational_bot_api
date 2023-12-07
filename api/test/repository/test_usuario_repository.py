import unittest
from mongomock import MongoClient
from ...src.infra.repository.mongodb_usuario_repository import MongodbUsuarioRepository
from ...src.domain.entities.usuario.usuario import Usuario, Role


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.mockclient = MongoClient()

    def tearDown(self):
        self.mockclient.close()

    def test_should_insert_an_user(self):
        user_repo = MongodbUsuarioRepository(self.mockclient)
        user = Usuario(id='123', discord_id='112233')
        user.grant_role(Role.DOCENTE)
        user_repo.insert(user)
        user_fetched = user_repo.get_by_id('123')
        self.assertIsInstance(user_fetched, Usuario)

    def test_should_raise_exception_when_user_dont_exists(self):
        user_repo = MongodbUsuarioRepository(self.mockclient)
        user = Usuario(id='123', discord_id='112233')
        user_repo.insert(user)
        user_fetched = user_repo.get_by_id('124')
        self.assertIsNone(user_fetched)

    def test_should_update_an_user(self):
        user_repo = MongodbUsuarioRepository(self.mockclient)
        user = Usuario(id='123', discord_id='112233')
        user.grant_role(Role.DOCENTE)
        user_repo.insert(user)
        result = user_repo.get_by_id('123')
        self.assertEqual(result.discord_id, '112233')
        result.discord_id = '112244'
        user_repo.update(result)
        result = user_repo.get_by_id('123')
        self.assertEqual(result.discord_id, '112244')


if __name__ == '__main__':
    unittest.main()
