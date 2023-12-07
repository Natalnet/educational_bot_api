import unittest
from api.src.domain.entities.usuario.usuario import Usuario, Role


class MyTestCase(unittest.TestCase):

    def test_should_create_an_user(self):
        user = Usuario(id='123', discord_id='112233')
        self.assertIsInstance(user, Usuario)

    def test_should_create_user_with_None_discord_id(self):
        user = Usuario(id='123')
        self.assertIsInstance(user, Usuario)

    def test_should_raise_exception_when_user_has_empty_id(self):
        with self.assertRaises(Exception) as ctx:
            Usuario(id='', discord_id='112233')
        self.assertEqual(str(ctx.exception), 'Id nao pode ser vazio')

    def test_subscribe_user_with_None_discord_id(self):
        user = Usuario(id='123')
        user.subscribe('112233')
        self.assertEqual(user.discord_id, '112233')

    def test_should_raise_exception_when_subccribe_user_with_invalid_discord_id(self):
        user = Usuario(id='123')
        with self.assertRaises(Exception) as ctx:
            user.subscribe('')
        self.assertEqual(str(ctx.exception), 'Discord Id invalido')
        with self.assertRaises(Exception) as ctx:
            user.subscribe(None)
        self.assertEqual(str(ctx.exception), 'Discord Id invalido')

    def test_should_grant_role_to_user(self):
        user = Usuario(id='123', discord_id='112233')
        user.grant_role(Role.DOCENTE)
        self.assertEqual(user.id, '123')
        self.assertEqual(user.discord_id, '112233')
        self.assertEqual(len(user.roles), 1)
        self.assertSetEqual(user.roles, {Role.DOCENTE})

    def test_should_revoke_role_from_user(self):
        user = Usuario(id='123', discord_id='112233')
        user.grant_role(Role.DOCENTE)
        user.revoke_role(Role.DOCENTE)
        self.assertEqual(len(user.roles), 0)


if __name__ == '__main__':
    unittest.main()
