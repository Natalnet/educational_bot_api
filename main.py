from fastapi import FastAPI
from src.routers import admin, pergunta, aluno, turma
from src.data.mongodb import connection

app = FastAPI()

@app.get("/health", status_code=200)
def health():
    try:
        client = connection
        db = client.test
        db.command("serverStatus")
        return {"status": "You are connected!"}
    except Exception as e:
        return {"status": e}

app.include_router(pergunta.router)

app.include_router(admin.router)

app.include_router(aluno.router)

app.include_router(turma.router)
