from datetime import date
from dataclasses import dataclass, field
from typing import List
from ..aluno.aluno import Aluno
from ..usuario.usuario import Usuario, Role
from ..miniteste.miniteste import Miniteste


@dataclass
class Turma:
    id: str
    denominacao: str
    ano: int
    periodo: int
    data_inicio: date
    data_fim: date
    esta_consolidada: bool = False
    docente: Usuario = None
    alunos: List[Aluno] = field(default_factory=list)
    monitores: List[Usuario] = field(default_factory=list)
    minitestes: List[Miniteste] = field(default_factory=list)

    def __post_init__(self):
        self.validate()

    def validate(self):
        if self.id == '':
            raise Exception('Id nao pode ser vazio')
        if self.denominacao == '':
            raise Exception('Denominacao nao permitida')
        if self.data_fim < self.data_inicio:
            raise Exception('Data fim deve ser apos a Data inicio da turma')

    def add_alunos(self, alunos: List[Aluno]):
        for aluno in alunos:
            self.alunos.append(aluno)

    def add_monitor(self, monitor: Usuario):
        if Role.MONITOR in monitor.roles:
            self.monitores.append(monitor)
        else:
            raise Exception(f'O usuario nao possui a role {Role.MONITOR}')

    def add_miniteste(self, minitestes: List[Miniteste]):
        for miniteste in minitestes:
            self.minitestes.append(miniteste)

    def consolidar(self):
        self.esta_consolidada = True

    def definir_docente(self, docente: Usuario):
        if Role.DOCENTE in docente.roles:
            self.docente = docente
        else:
            raise Exception(f'O usuario nao possui a role {Role.DOCENTE}')

    def to_dict(self):
        return {
            '_id': self.id,
            'denominacao': self.denominacao,
            'ano': self.ano,
            'periodo': self.periodo,
            'data_inicio': self.data_inicio.isoformat(),
            'data_fim': self.data_fim.isoformat(),
            'esta_consolidada': self.esta_consolidada,
            'docente': self.docente.id if self.docente is not None else None,
            'alunos': [aluno.to_dict() for aluno in self.alunos],
            'monitores': [monitor.id for monitor in self.monitores],
            'minitestes': [miniteste.to_dict() for miniteste in self.minitestes]
        }

    @classmethod
    def from_dict(cls, result):
        # alunos = result.get('alunos', [])
        # alunos_objects = [Aluno(**aluno) for aluno in alunos]

        return cls(id=result['_id'],
                  denominacao=result['denominacao'],
                  ano=result['ano'],
                  periodo=result['periodo'],
                  data_inicio=date.fromisoformat(result['data_inicio']),
                  data_fim=date.fromisoformat(result['data_fim']),
                  esta_consolidada=result['esta_consolidada'],
                  alunos=[Aluno.from_dict(aluno) for aluno in result.get('alunos', [])],
                  minitestes=[Miniteste.from_dict(miniteste) for miniteste in result.get('minitestes', [])]
                )
