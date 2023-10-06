from pydantic import BaseModel

class Miniteste(BaseModel):
    teste_id: str
    pergunta: str
    alternativas: object