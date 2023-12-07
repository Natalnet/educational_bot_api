from dataclasses import dataclass

@dataclass
class Alternativas:
    A: str
    B: str
    C: str
    D: str

    def __post_init__(self):
        self.validate()

    def validate(self):
        if self.A == '' or self.B == '' or self.C == '' or self.D == '':
            raise Exception('Alternativa nao pode ser vazia')

    def to_dict(self):
        return {
            'A': self.A,
            'B': self.B,
            'C': self.C,
            'D': self.D
        }