from dataclasses import dataclass

@dataclass
class MinitesteResult:
    teste_id: str
    opcao: str
    status: bool