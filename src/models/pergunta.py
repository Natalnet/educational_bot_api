from pydantic import BaseModel

class Pergunta(BaseModel):
    pergunta: str
    resposta: str

    def validate(self):
        if self.pergunta is None or self.resposta is None:
            return False
        return True