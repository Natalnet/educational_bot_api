from pydantic import BaseModel


class AlternativasDto(BaseModel):
    A: str
    B: str
    C: str
    D: str


class MinitestesDto(BaseModel):
    teste_id: str
    pergunta: str
    resposta: str
    alternativas: AlternativasDto


class ResponderMinitesteDto(BaseModel):
    teste_id: str
    opcao: str
