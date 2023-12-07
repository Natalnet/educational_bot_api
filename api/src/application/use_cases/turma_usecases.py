from datetime import date
from typing import List
from uuid import uuid4
from api.src.application.dto.miniteste_dto import MinitestesDto, ResponderMinitesteDto
from api.src.application.dto.presenca_aluno_dto import PresencaAlunoDto
from api.src.application.dto.turma_dto_input import TurmaDtoInput, AlunoDto
from api.src.application.dto.turma_dto_output import TurmaDtoOutput
from api.src.domain.entities.aluno.aluno import Aluno
from api.src.domain.entities.aluno.minitest_result import MinitesteResult
from api.src.domain.entities.miniteste.miniteste import Miniteste, Alternativas
from api.src.domain.entities.turma.turma import Turma
from api.src.domain.entities.usuario.usuario import Usuario, Role
from api.src.domain.repository.abstract_turma_repository import AbstractTurmaRepository
from api.src.domain.repository.abstract_usuario_repository import AbstractUsuarioRepository
from api.src.domain.exceptions.exceptions import (
    TurmaNotFoundException,
    UserNotFoundException
)


class CadastrarTurmaUseCase():
    def __init__(self, turma_repository: AbstractTurmaRepository,
                 usuario_repository: AbstractUsuarioRepository):
        self.turma_repository = turma_repository
        self.usuario_repository = usuario_repository

    def execute(self, turma_dto_input: TurmaDtoInput) -> TurmaDtoOutput:
        turma = Turma(id=str(uuid4()),
                      denominacao=turma_dto_input.denominacao,
                      ano=turma_dto_input.ano,
                      periodo=turma_dto_input.periodo,
                      data_inicio=date.fromisoformat(turma_dto_input.data_inicio),
                      data_fim=date.fromisoformat(turma_dto_input.data_fim))
        alunos = [Aluno(str(uuid4()), aluno.nome, aluno.matricula, aluno.turma)
                  for aluno in turma_dto_input.alunos]
        turma.add_alunos(alunos)

        self.turma_repository.insert(turma)
        for aluno in turma.alunos:
            user_fetched = self.usuario_repository.get_by_id(aluno.id)
            if user_fetched is None:
                new_user = Usuario(id=aluno.id)
                new_user.grant_role(Role.DISCENTE)
                self.usuario_repository.insert(new_user)
            else:
                user_fetched.id = aluno.id
                user_fetched.grant_role(Role.DISCENTE)
                self.usuario_repository.update(user_fetched)

        return TurmaDtoOutput(id=turma.id, denominacao=turma.denominacao)


class CadastrarAlunoEmTurmaUseCase():
    def __init__(self, turma_repository: AbstractTurmaRepository,
                 usuario_repository: AbstractUsuarioRepository):
        self.turma_repository = turma_repository
        self.usuario_repository = usuario_repository

    def execute(self, turma_id: str, alunos_dto: List[AlunoDto]) -> None:
        turma_fetched = self.turma_repository.get_by_id(turma_id)
        if turma_fetched is None:
            raise TurmaNotFoundException

        alunos = [Aluno(str(uuid4()), aluno.nome, aluno.matricula, aluno.turma)
                  for aluno in alunos_dto]
        turma_fetched.add_alunos(alunos)
        self.turma_repository.update(turma_fetched)

        for aluno in alunos:
            user_fetched = self.usuario_repository.get_by_id(aluno.id)
            if user_fetched is None:
                new_user = Usuario(id=aluno.id)
                new_user.grant_role(Role.DISCENTE)
                self.usuario_repository.insert(new_user)
            else:
                user_fetched.id = aluno.id
                user_fetched.grant_role(Role.DISCENTE)
                self.usuario_repository.update(user_fetched)


class AddDocenteToTurmaUseCase():
    def __init__(self, turma_repository: AbstractTurmaRepository,
                 usuario_repository: AbstractUsuarioRepository):
        self.turma_repository = turma_repository
        self.usuario_repository = usuario_repository

    def execute(self, turma_id: str, docente_discord_id: str) -> None:
        turma_fetched = self.turma_repository.get_by_id(turma_id)
        if turma_fetched is None:
            raise TurmaNotFoundException

        user_fetched = self.usuario_repository.get_by_discord_id(docente_discord_id)
        if user_fetched is None:
            raise UserNotFoundException

        turma_fetched.definir_docente(user_fetched)
        self.turma_repository.update(turma_fetched)


class AddMonitorToTurmaUseCase():
    def __init__(self, turma_repository: AbstractTurmaRepository,
                 usuario_repository: AbstractUsuarioRepository):
        self.turma_repository = turma_repository
        self.usuario_repository = usuario_repository

    def execute(self, turma_id: str, monitor_discord_id: str) -> None:
        turma_fetched = self.turma_repository.get_by_id(turma_id)
        if turma_fetched is None:
            raise TurmaNotFoundException

        user_fetched = self.usuario_repository.get_by_discord_id(monitor_discord_id)
        if user_fetched is None:
            raise UserNotFoundException

        turma_fetched.add_monitor(user_fetched)
        self.turma_repository.update(turma_fetched)


class AddMinitesteToTurma():
    def __init__(self, turma_repository: AbstractTurmaRepository):
        self.turma_repository = turma_repository

    def execute(self, turma_id: str, minitestes_dto: List[MinitestesDto]) -> None:
        turma_fetched = self.turma_repository.get_by_id(turma_id)
        if turma_fetched is None:
            raise TurmaNotFoundException

        minitestes = []
        for miniteste in minitestes_dto:
            minitestes.append(Miniteste(id=str(uuid4()),
                                        teste_id=miniteste.teste_id,
                                        pergunta=miniteste.pergunta,
                                        resposta=miniteste.resposta,
                                        alternativas=Alternativas(
                                            A=miniteste.alternativas.A,
                                            B=miniteste.alternativas.B,
                                            C=miniteste.alternativas.C,
                                            D=miniteste.alternativas.D)
                                        )
                              )
        turma_fetched.add_miniteste(minitestes)
        self.turma_repository.update(turma_fetched)


class RegistrarPresencaUseCase():
    def __init__(self, turma_repository: AbstractTurmaRepository,
                 usuario_repository: AbstractUsuarioRepository):
        self.turma_repository = turma_repository
        self.usuario_repository = usuario_repository

    def execute(self, turma_id: str, discord_id: str) -> None:
        turma_fetched = self.turma_repository.get_by_id(turma_id)
        if turma_fetched is None:
            raise TurmaNotFoundException

        aluno_fetched = self.usuario_repository.get_by_discord_id(discord_id)
        if aluno_fetched is None:
            raise UserNotFoundException

        for aluno in turma_fetched.alunos:
            if aluno.id == aluno_fetched.id:
                aluno.registrar_presenca(date.today())
                break

        self.turma_repository.update(turma_fetched)


class ResponderMinitesteUseCase():
    def __init__(self, turma_repository: AbstractTurmaRepository,
                 usuario_repository: AbstractUsuarioRepository):
        self.turma_repository = turma_repository
        self.usuario_repository = usuario_repository

    def execute(self, turma_id: str, discord_id: str,
                resposta_miniteste_dto: ResponderMinitesteDto) -> bool:
        turma_fetched = self.turma_repository.get_by_id(turma_id)
        if turma_fetched is None:
            raise TurmaNotFoundException

        aluno_fetched = self.usuario_repository.get_by_discord_id(discord_id)
        if aluno_fetched is None:
            raise Exception('Aluno nao foi encontrado')

        aluno_to_answer = None
        minitest_to_answer = None

        for miniteste in turma_fetched.minitestes:
            if miniteste.teste_id == resposta_miniteste_dto.teste_id:
                minitest_to_answer = miniteste
                break

        for aluno in turma_fetched.alunos:
            if aluno.id == aluno_fetched.id:
                aluno_to_answer = aluno
                break

        miniteste_status = minitest_to_answer.responder(resposta_miniteste_dto.opcao)
        result = MinitesteResult(teste_id=resposta_miniteste_dto.teste_id,
                                 opcao=resposta_miniteste_dto.opcao,
                                 status=miniteste_status)
        aluno_to_answer.responder_minitest(result)
        self.turma_repository.update(turma_fetched)
        return miniteste_status


class ObterFrequenciaTurmaUseCase():
    def __init__(self, turma_repository: AbstractTurmaRepository):
        self.turma_repository = turma_repository

    def execute(self, turma_id: str) -> List[PresencaAlunoDto]:
        turma_fetched = self.turma_repository.get_by_id(turma_id)

        if turma_fetched is None:
            raise TurmaNotFoundException

        dados = []
        for aluno in turma_fetched.alunos:
            freq = [date.isoformat(freq) for freq in aluno.frequencias]
            dado = PresencaAlunoDto(nome=aluno.nome,
                                    matricula=aluno.matricula,
                                    frequencia=freq)
            dados.append(dado)
        return dados
