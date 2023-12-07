
from dataclasses import dataclass, field
from datetime import date
from typing import List
from api.src.domain.entities.aluno.minitest_result import MinitesteResult
from api.src.domain.exceptions.exceptions import InvalidDateRegistrarPresencaException


@dataclass
class Aluno:
    id: str
    nome: str
    matricula: str
    turma: str
    frequencias: List[date] = field(default_factory=list)
    minitestes: List[MinitesteResult] = field(default_factory=list)

    def __post_init__(self):
        self.validate()

    def validate(self):
        if self.id == '':
            raise Exception('Id nao pode ser vazio')
        if self.nome == '':
            raise Exception('Nome nao pode ser vazio')
        if self.matricula == '':
            raise Exception('Matricula nao pode ser vazio')
        if self.turma == '':
            raise Exception('Turma nao pode ser vazio')

    def registrar_presenca(self, today: date) -> None:
        if today in self.frequencias:
            raise InvalidDateRegistrarPresencaException(today)
        self.frequencias.append(today)

    def responder_minitest(self, minitest_result: MinitesteResult):
        self.minitestes.append(minitest_result)

    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            'matricula': self.matricula,
            'turma': self.turma,
            'frequencias': [
                freq.isoformat() for freq in self.frequencias
            ],
            'minitestes': [
                {
                    "teste_id": minitest_result.teste_id,
                    "opcao": minitest_result.opcao,
                    "status": minitest_result.status
                }
                for minitest_result in self.minitestes
            ]
        }

    @classmethod
    def from_dict(cls, aluno):
        return cls(id=aluno['id'],
                   nome=aluno['nome'],
                   matricula=aluno['matricula'],
                   turma=aluno['turma'],
                   frequencias=[date.fromisoformat(freq) for freq in aluno.get('frequencias', [])],
                   minitestes=[MinitesteResult(**miniteste) for miniteste in aluno.get('minitestes', [])]
                   )

