from pydantic import BaseModel

class Turma(BaseModel):
    denominacao: str
    ano: int
    periodo: int
    # esta_consolidada: bool = False
    data_inicio: str
    data_fim: str
    docente: str
    # monitores: list
    alunos: list
    # minitestes: list