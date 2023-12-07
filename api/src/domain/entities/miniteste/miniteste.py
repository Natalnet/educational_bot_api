
from dataclasses import dataclass
from .alternativas import Alternativas

@dataclass
class Miniteste:
    id: str
    teste_id: str
    pergunta: str
    resposta: str
    alternativas: Alternativas
    total_respostas: int = 0
    total_acertos: int = 0

    def __post_init__(self):
        self.validate()

    def validate(self):
        if self.id == '':
            raise Exception('Id nao pode ser vazio')
        if self.teste_id == '':
            raise Exception('Teste Id nao pode ser vazio')
        if self.pergunta == '':
            raise Exception('Pergunta nao pode ser vazio')
        if self.resposta == '':
            raise Exception('Resposta nao pode ser vazio')

    def responder(self, opcao: str):
        if opcao == self.resposta:
            self.total_acertos += 1
            self.total_respostas += 1
            return True
        else:
            self.total_respostas += 1
            return False

    def get_taxa_acertos(self):
        return self.total_acertos / self.total_respostas

    def to_dict(self):
        return {
            "id": self.id,
            "teste_id": self.teste_id,
            "pergunta": self.pergunta,
            "resposta": self.resposta,
            "total_respostas": self.total_respostas,
            "total_acertos": self.total_acertos,
            "alternativas": self.alternativas.to_dict()
        }

    @classmethod
    def from_dict(cls, miniteste):
        return cls(id=miniteste['id'],
                   teste_id=miniteste['teste_id'],
                   pergunta=miniteste['pergunta'],
                   resposta=miniteste['resposta'],
                   total_acertos=miniteste['total_acertos'],
                   total_respostas=miniteste['total_respostas'],
                   alternativas=Alternativas(
                       A=miniteste['alternativas']['A'],
                       B=miniteste['alternativas']['B'],
                       C=miniteste['alternativas']['C'],
                       D=miniteste['alternativas']['D'],)
                   )
