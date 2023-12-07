from dataclasses import dataclass, field
from typing import List

# @dataclass()
# class TurmaModel:
#     id: str
#     denominacao: str
#     ano: int
#     periodo: int
#     data_inicio: date
#     data_fim: date
#     esta_consolidada: bool = False
#     docente: Usuario = None
#     alunos: List[Aluno] = field(default_factory=list)
#     monitores: List[Usuario] = field(default_factory=list)
#     minitestes: List[Miniteste] = field(default_factory=list)
#
#     def to_dict(self):
#         return {
#             'id': self.id,
#             'denominacao': self.denominacao,
#             'ano': self.ano,
#             'periodo': self.periodo,
#             'data_inicio': self.data_inicio,
#             'data_fim': self.data_fim,
#             'esta_consolidada': self.esta_consolidada
#         }