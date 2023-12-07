from fastapi import FastAPI
from api.src.infra.routers.turma_router import router as turma_router
from api.src.infra.routers.usuario_router import router as user_router

app = FastAPI()

app.include_router(turma_router)
app.include_router(user_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)