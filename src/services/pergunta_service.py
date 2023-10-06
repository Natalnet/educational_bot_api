from uuid import uuid4
from src.data.mongodb import connection
from src.models.pergunta import Pergunta

class PerguntaService():
    
    def __init__(self):
        client = connection
        db = client.apibotdb
        self.collection = db.perguntas

    def adicionar(self, pergunta: Pergunta):
        if not pergunta.validate():
            return Exception

        self.collection.insert_one({
            '_id': str(uuid4()),
            'pergunta': pergunta.pergunta,
            'resposta': pergunta.resposta
        })

    def perguntar(self, texto: str):
        # realiza uma pergunta para o motor NLP
        pass