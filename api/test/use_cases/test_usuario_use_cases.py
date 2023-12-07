import unittest
from mongomock import MongoClient
from api.src.application.dto.turma_dto_input import TurmaDtoInput, AlunoDto
from api.src.application.dto.user_dto import UserDtoInput
from api.src.domain.entities.usuario.usuario import Usuario, Role
from api.src.infra.repository.mongodb_turma_repository import MongodbTurmaRepository
from api.src.infra.repository.mongodb_usuario_repository import MongodbUsuarioRepository
from api.src.application.use_cases.turma_usecases import CadastrarTurmaUseCase
from api.src.application.use_cases.usuario_usecases import (
    CreateUserUseCase,
    GrantRoleToUsuario,
    RevokeRoleFromUsuario,
    RegistrarAlunoUseCase
)


class MyTestCase(unittest.TestCase):
    def setUp(self):
        self.client = MongoClient()

    def tearDown(self):
        self.client.close()

    def test_create_an_new_user(self):
        usuario_repository = MongodbUsuarioRepository(self.client)
        create_user_usecase = CreateUserUseCase(usuario_repository)

        user_input = UserDtoInput(discord_id='112233')
        user_output = create_user_usecase.execute(user_input)

        user_fetched = usuario_repository.get_by_id(user_output.id)
        self.assertIsNotNone(user_fetched.id)
        self.assertEqual(user_fetched.discord_id, '112233')

    def test_grant_role_to_user(self):
        usuario_repository = MongodbUsuarioRepository(self.client)
        create_user_usecase = CreateUserUseCase(usuario_repository)
        grant_role_usercase = GrantRoleToUsuario(usuario_repository)

        user_input = UserDtoInput(discord_id='112233')
        user_output = create_user_usecase.execute(user_input)

        grant_role_usercase.execute(user_output.discord_id, 'DOCENTE')

        user_fetched = usuario_repository.get_by_id(user_output.id)
        self.assertIsInstance(user_fetched, Usuario)
        self.assertIsNotNone(user_fetched.id)
        self.assertIn(Role.DOCENTE, user_fetched.roles)

        grant_role_usercase.execute(user_output.discord_id, 'ADMIN')

        user_fetched = usuario_repository.get_by_id(user_output.id)
        self.assertIn(Role.DOCENTE, user_fetched.roles)
        self.assertIn(Role.ADMIN, user_fetched.roles)

    def test_revoke_role_from_user(self):
        usuario_repository = MongodbUsuarioRepository(self.client)
        create_user_usecase = CreateUserUseCase(usuario_repository)
        grant_role_usercase = GrantRoleToUsuario(usuario_repository)
        revoke_role_user_case = RevokeRoleFromUsuario(usuario_repository)

        user_input = UserDtoInput(discord_id='112233')
        user_output = create_user_usecase.execute(user_input)

        grant_role_usercase.execute(user_output.discord_id, 'DOCENTE')
        revoke_role_user_case.execute(user_output.discord_id, 'DOCENTE')

        user_fetched = usuario_repository.get_by_id(user_output.id)
        self.assertNotIn(Role.DOCENTE, user_fetched.roles)

    def test_subscribe_user_when_its_auregistrated_as_aluno(self):
        usuario_repository = MongodbUsuarioRepository(self.client)
        turma_repository = MongodbTurmaRepository(self.client)
        create_turma_usecase = CadastrarTurmaUseCase(turma_repository, usuario_repository)
        register_aluno_usecase = RegistrarAlunoUseCase(usuario_repository, turma_repository)

        turma_input = TurmaDtoInput(denominacao='LOP_Orivaldo',
                                    ano=2023,
                                    periodo=2,
                                    data_inicio='2023-10-02',
                                    data_fim='2023-12-02',
                                    alunos=[
                                        AlunoDto(nome='Joao',
                                                 matricula='111222',
                                                 turma='2A'),
                                        AlunoDto(nome='Maria',
                                                 matricula='111223',
                                                 turma='1B')
                                    ])

        turma_output = create_turma_usecase.execute(turma_input)

        turma_fetch = turma_repository.get_by_id(turma_output.id)

        user_fetched = usuario_repository.get_by_id(turma_fetch.alunos[0].id)
        self.assertIsNone(user_fetched.discord_id)
        user_fetched = usuario_repository.get_by_id(turma_fetch.alunos[1].id)
        self.assertIsNone(user_fetched.discord_id)

        register_aluno_usecase.execute(turma_output.id, 'discord123', turma_fetch.alunos[0].matricula)

        user_fetched = usuario_repository.get_by_id(turma_fetch.alunos[0].id)
        self.assertEqual(user_fetched.discord_id, 'discord123')
        user_fetched = usuario_repository.get_by_id(turma_fetch.alunos[1].id)
        self.assertIsNone(user_fetched.discord_id)

        register_aluno_usecase.execute(turma_output.id, 'discord321', turma_fetch.alunos[1].matricula)

        user_fetched = usuario_repository.get_by_id(turma_fetch.alunos[0].id)
        self.assertEqual(user_fetched.discord_id, 'discord123')
        user_fetched = usuario_repository.get_by_id(turma_fetch.alunos[1].id)
        self.assertEqual(user_fetched.discord_id, 'discord321')


if __name__ == '__main__':
    unittest.main()
