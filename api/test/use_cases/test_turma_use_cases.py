import unittest
from datetime import date
from typing import List
from uuid import uuid4
from mongomock import MongoClient
from api.src.application.dto.miniteste_dto import MinitestesDto, AlternativasDto, ResponderMinitesteDto
from api.src.application.dto.presenca_aluno_dto import PresencaAlunoDto
from api.src.application.dto.turma_dto_input import TurmaDtoInput, AlunoDto
from api.src.application.dto.user_dto import UserDtoInput
from api.src.domain.exceptions.exceptions import TurmaNotFoundException
from api.src.domain.entities.aluno.minitest_result import MinitesteResult
from api.src.domain.entities.usuario.usuario import Usuario
from api.src.infra.repository.mongodb_turma_repository import MongodbTurmaRepository
from api.src.infra.repository.mongodb_usuario_repository import MongodbUsuarioRepository
from api.src.application.use_cases.usuario_usecases import RegistrarAlunoUseCase
from api.src.application.use_cases.turma_usecases import (
    CadastrarTurmaUseCase,
    CadastrarAlunoEmTurmaUseCase,
    AddDocenteToTurmaUseCase,
    RegistrarPresencaUseCase,
    ResponderMinitesteUseCase,
    AddMonitorToTurmaUseCase,
    AddMinitesteToTurma,
    ObterFrequenciaTurmaUseCase
)
from api.src.application.use_cases.usuario_usecases import (
    CreateUserUseCase,
    GrantRoleToUsuario
)


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.client = MongoClient()

    def tearDown(self):
        self.client.close()

    def test_create_a_turma(self):
        turma_reposity = MongodbTurmaRepository(self.client)
        usuario_repository = MongodbUsuarioRepository(self.client)
        create_turma_use_case = CadastrarTurmaUseCase(turma_reposity, usuario_repository)

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

        turma_dto_output = create_turma_use_case.execute(turma_input)
        self.assertEqual(len(usuario_repository.list()), 2)
        self.assertIsNotNone(turma_dto_output.id)
        self.assertEqual(turma_dto_output.denominacao, 'LOP_Orivaldo')

    def test_insert_alunos_in_turma(self):
        turma_reposity = MongodbTurmaRepository(self.client)
        usuario_repository = MongodbUsuarioRepository(self.client)
        create_turma_use_case = CadastrarTurmaUseCase(turma_reposity, usuario_repository)
        cadastrar_alunos_em_turma_use_case = CadastrarAlunoEmTurmaUseCase(turma_reposity, usuario_repository)

        turma_input = TurmaDtoInput(denominacao='LOP_Orivaldo',
                                    ano=2023,
                                    periodo=2,
                                    data_inicio='2023-10-02',
                                    data_fim='2023-12-02',
                                    alunos=[
                                        AlunoDto(nome='Joao',
                                                 matricula='111222',
                                                 turma='2A')
                                    ])

        turma_dto_output = create_turma_use_case.execute(turma_input)

        alunos_input = [
            AlunoDto(nome='Maria',
                     matricula='111223',
                     turma='1B'),
            AlunoDto(nome='Pedro',
                     matricula='111224',
                     turma='2C')
        ]

        cadastrar_alunos_em_turma_use_case.execute(turma_dto_output.id, alunos_input)
        turma_fetched = turma_reposity.get_by_id(turma_dto_output.id)
        self.assertEqual(len(turma_fetched.alunos), 3)
        self.assertIsNotNone(turma_fetched.alunos[0].id)
        self.assertEqual(turma_fetched.alunos[0].matricula, '111222')
        self.assertIsNotNone(turma_fetched.alunos[1].id)
        self.assertEqual(turma_fetched.alunos[1].matricula, '111223')
        self.assertIsNotNone(turma_fetched.alunos[2].id)
        self.assertEqual(turma_fetched.alunos[2].matricula, '111224')
        self.assertEqual(len(usuario_repository.list()), 3)

        with self.assertRaises(TurmaNotFoundException) as ctx:
            cadastrar_alunos_em_turma_use_case.execute(str(uuid4()), alunos_input)

    def test_add_docente_to_turma(self):
        turma_reposity = MongodbTurmaRepository(self.client)
        usuario_repository = MongodbUsuarioRepository(self.client)
        create_turma_usecase = CadastrarTurmaUseCase(turma_reposity, usuario_repository)
        create_user_usecase = CreateUserUseCase(usuario_repository)
        grant_role_usecase = GrantRoleToUsuario(usuario_repository)

        turma_input = TurmaDtoInput(denominacao='LOP_Orivaldo',
                                    ano=2023,
                                    periodo=2,
                                    data_inicio='2023-10-02',
                                    data_fim='2023-12-02',
                                    alunos=[
                                        AlunoDto(nome='Joao',
                                                 matricula='111222',
                                                 turma='2A')
                                    ])

        turma_dto_output = create_turma_usecase.execute(turma_input)

        turma_fetched = turma_reposity.get_by_id(turma_dto_output.id)
        self.assertIsNone(turma_fetched.docente)

        user_input = UserDtoInput(discord_id='112233')
        user_output = create_user_usecase.execute(user_input)
        grant_role_usecase.execute(user_output.discord_id, 'DOCENTE')

        add_docente_to_turma = AddDocenteToTurmaUseCase(turma_reposity, usuario_repository)
        add_docente_to_turma.execute(turma_dto_output.id, user_output.discord_id)

        turma_fetched = turma_reposity.get_by_id(turma_dto_output.id)
        self.assertIsNotNone(turma_fetched.docente)
        self.assertIsInstance(turma_fetched.docente, Usuario)
        self.assertEqual(turma_fetched.docente.id, user_output.id)

    def test_add_monitor_to_turma(self):
        turma_reposity = MongodbTurmaRepository(self.client)
        usuario_repository = MongodbUsuarioRepository(self.client)
        create_turma_usecase = CadastrarTurmaUseCase(turma_reposity, usuario_repository)
        create_user_usecase = CreateUserUseCase(usuario_repository)
        grant_role_usecase = GrantRoleToUsuario(usuario_repository)

        turma_input = TurmaDtoInput(denominacao='LOP_Orivaldo',
                                    ano=2023,
                                    periodo=2,
                                    data_inicio='2023-10-02',
                                    data_fim='2023-12-02',
                                    alunos=[
                                        AlunoDto(nome='Joao',
                                                 matricula='111222',
                                                 turma='2A')
                                    ])

        turma_dto_output = create_turma_usecase.execute(turma_input)

        turma_fetched = turma_reposity.get_by_id(turma_dto_output.id)
        self.assertSequenceEqual(turma_fetched.monitores, [])

        user_input = UserDtoInput(discord_id='112233')
        user_output = create_user_usecase.execute(user_input)
        grant_role_usecase.execute(user_output.discord_id, 'MONITOR')

        add_monitor_to_turma = AddMonitorToTurmaUseCase(turma_reposity, usuario_repository)
        add_monitor_to_turma.execute(turma_dto_output.id, user_output.discord_id)

        turma_fetched = turma_reposity.get_by_id(turma_dto_output.id)
        self.assertIsInstance(turma_fetched.monitores[0], Usuario)
        self.assertEqual(len(turma_fetched.monitores), 1)
        self.assertEqual(turma_fetched.monitores[0].id, user_output.id)

    def test_add_minitestes_to_turma(self):
        turma_reposity = MongodbTurmaRepository(self.client)
        usuario_repository = MongodbUsuarioRepository(self.client)
        add_minitestes_usercase = AddMinitesteToTurma(turma_reposity)
        create_turma_use_case = CadastrarTurmaUseCase(turma_reposity, usuario_repository)

        turma_input = TurmaDtoInput(denominacao='LOP_Orivaldo',
                                    ano=2023,
                                    periodo=2,
                                    data_inicio='2023-10-02',
                                    data_fim='2023-12-02',
                                    alunos=[])

        turma_output = create_turma_use_case.execute(turma_input)

        m1 = MinitestesDto(teste_id='T01',
                           pergunta='pergunta 1',
                           resposta='B',
                           alternativas=AlternativasDto(
                               A='alternativa A',
                               B='alternativa B',
                               C='alternativa C',
                               D='alternativa D'
                           ))
        m2 = MinitestesDto(teste_id='T02',
                           pergunta='pergunta 2',
                           resposta='A',
                           alternativas=AlternativasDto(
                               A='alternativa A',
                               B='alternativa B',
                               C='alternativa C',
                               D='alternativa D'
                           ))

        add_minitestes_usercase.execute(turma_id=turma_output.id, minitestes_dto=[m1, m2])
        turma_fetch = turma_reposity.get_by_id(turma_output.id)
        print(turma_fetch)
        self.assertEqual(len(turma_fetch.minitestes), 2)

    def test_registrar_presenca(self):
        turma_repository = MongodbTurmaRepository(self.client)
        usuario_repository = MongodbUsuarioRepository(self.client)
        create_turma_usecase = CadastrarTurmaUseCase(turma_repository, usuario_repository)
        register_aluno_usecase = RegistrarAlunoUseCase(usuario_repository, turma_repository)
        registrar_presenca_usecase = RegistrarPresencaUseCase(turma_repository, usuario_repository)

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

        register_aluno_usecase.execute(turma_output.id, '445566', turma_input.alunos[0].matricula)

        registrar_presenca_usecase.execute(turma_id=turma_output.id, discord_id='445566')

        alunos = turma_repository.get_by_id(turma_output.id).alunos
        aluno = alunos[0]

        self.assertEqual(len(aluno.frequencias), 1)
        self.assertIsInstance(aluno.frequencias[0], date)
        self.assertEqual(aluno.frequencias[0], date.today())

        with self.assertRaises(Exception) as ctx:
            registrar_presenca_usecase.execute(turma_id=turma_output.id, discord_id='445566')
        self.assertEqual(str(ctx.exception), f'Presença ja cadastrada na data {date.today()}')

    def test_responder_pergunta_corretamente(self):
        turma_repository = MongodbTurmaRepository(self.client)
        usuario_repository = MongodbUsuarioRepository(self.client)
        create_turma_usecase = CadastrarTurmaUseCase(turma_repository, usuario_repository)
        add_minitestes_usecase = AddMinitesteToTurma(turma_repository)
        register_aluno_usecase = RegistrarAlunoUseCase(usuario_repository, turma_repository)
        responder_miniteste_usecase = ResponderMinitesteUseCase(turma_repository, usuario_repository)

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

        m1 = MinitestesDto(teste_id='T01',
                           pergunta='pergunta 1',
                           resposta='B',
                           alternativas=AlternativasDto(
                               A='alternativa A',
                               B='alternativa B',
                               C='alternativa C',
                               D='alternativa D'
                           ))
        m2 = MinitestesDto(teste_id='T02',
                           pergunta='pergunta 2',
                           resposta='A',
                           alternativas=AlternativasDto(
                               A='alternativa A',
                               B='alternativa B',
                               C='alternativa C',
                               D='alternativa D'
                           ))

        add_minitestes_usecase.execute(turma_id=turma_output.id, minitestes_dto=[m1, m2])

        turma_fetch = turma_repository.get_by_id(turma_output.id)

        register_aluno_usecase.execute(turma_fetch.id, '445566', turma_input.alunos[0].matricula)
        responder_miniteste_usecase.execute(discord_id='445566',
                                            turma_id=turma_fetch.id,
                                            resposta_miniteste_dto=ResponderMinitesteDto(teste_id='T02', opcao='A'))

        turma_fetch = turma_repository.get_by_id(turma_fetch.id)

        minitestes = turma_fetch.minitestes
        miniteste = minitestes[1]
        self.assertEqual(miniteste.total_acertos, 1)
        self.assertEqual(miniteste.total_respostas, 1)

        alunos = turma_fetch.alunos
        aluno = alunos[0]
        self.assertEqual(len(aluno.minitestes), 1)
        self.assertIsInstance(aluno.minitestes[0], MinitesteResult)
        self.assertEqual(aluno.minitestes[0].teste_id, 'T02')
        self.assertEqual(aluno.minitestes[0].status, True)

    def test_responder_pergunta_incorretamente(self):
        turma_repository = MongodbTurmaRepository(self.client)
        usuario_repository = MongodbUsuarioRepository(self.client)
        create_turma_usecase = CadastrarTurmaUseCase(turma_repository, usuario_repository)
        add_minitestes_usecase = AddMinitesteToTurma(turma_repository)
        register_aluno_usecase = RegistrarAlunoUseCase(usuario_repository, turma_repository)
        responder_miniteste_usecase = ResponderMinitesteUseCase(turma_repository, usuario_repository)

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

        m1 = MinitestesDto(teste_id='T01',
                           pergunta='pergunta 1',
                           resposta='B',
                           alternativas=AlternativasDto(
                               A='alternativa A',
                               B='alternativa B',
                               C='alternativa C',
                               D='alternativa D'
                           ))
        m2 = MinitestesDto(teste_id='T02',
                           pergunta='pergunta 2',
                           resposta='A',
                           alternativas=AlternativasDto(
                               A='alternativa A',
                               B='alternativa B',
                               C='alternativa C',
                               D='alternativa D'
                           ))

        add_minitestes_usecase.execute(turma_id=turma_output.id, minitestes_dto=[m1, m2])

        turma_fetch = turma_repository.get_by_id(turma_output.id)

        register_aluno_usecase.execute(turma_fetch.id, '445566', turma_input.alunos[0].matricula)
        responder_miniteste_usecase.execute(discord_id='445566',
                                            turma_id=turma_fetch.id,
                                            resposta_miniteste_dto=ResponderMinitesteDto(teste_id='T02', opcao='C'))

        turma_fetch = turma_repository.get_by_id(turma_fetch.id)

        minitestes = turma_fetch.minitestes
        miniteste = minitestes[1]
        self.assertEqual(miniteste.total_acertos, 0)
        self.assertEqual(miniteste.total_respostas, 1)

        alunos = turma_fetch.alunos
        aluno = alunos[0]
        self.assertEqual(len(aluno.minitestes), 1)
        self.assertIsInstance(aluno.minitestes[0], MinitesteResult)
        self.assertEqual(aluno.minitestes[0].teste_id, 'T02')
        self.assertEqual(aluno.minitestes[0].status, False)

    def test_obter_freq_turma(self):
        turma_repository = MongodbTurmaRepository(self.client)
        usuario_repository = MongodbUsuarioRepository(self.client)
        create_turma_usecase = CadastrarTurmaUseCase(turma_repository, usuario_repository)
        register_aluno_usecase = RegistrarAlunoUseCase(usuario_repository, turma_repository)
        registrar_presenca_usecase = RegistrarPresencaUseCase(turma_repository, usuario_repository)
        obter_freq_turma_usecase = ObterFrequenciaTurmaUseCase(turma_repository)

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

        register_aluno_usecase.execute(turma_output.id, '445566', turma_input.alunos[0].matricula)
        register_aluno_usecase.execute(turma_output.id, '445567', turma_input.alunos[1].matricula)

        registrar_presenca_usecase.execute(turma_id=turma_output.id, discord_id='445566')
        registrar_presenca_usecase.execute(turma_id=turma_output.id, discord_id='445567')

        lista_presenca: List[PresencaAlunoDto] = obter_freq_turma_usecase.execute(turma_output.id)

        self.assertEqual(len(lista_presenca), 2)
        self.assertEqual(lista_presenca[0].nome, 'Joao')
        self.assertEqual(lista_presenca[0].matricula, '111222')
        self.assertEqual(lista_presenca[0].frequencia, [str(date.today())])
        self.assertEqual(lista_presenca[1].nome, 'Maria')
        self.assertEqual(lista_presenca[1].matricula, '111223')
        self.assertEqual(lista_presenca[1].frequencia, [str(date.today())])


if __name__ == '__main__':
    unittest.main()
