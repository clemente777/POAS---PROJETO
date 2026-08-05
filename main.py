from fastapi import FastAPI
from backend.models import *
from fastapi.middleware.cors import CORSMiddleware

from fastapi.exceptions import RequestValidationError
from backend.exceptions.handlers import tratar_validacao

from backend.database.seed import criar_admin

from backend.routes import (
    cadastro_routes,
    usuario_routes,
    login_routes,
    logout_routes,
    cliente_routes,
    animal_routes,
    agendamento_routes,
    atendimento_routes,
    produto_routes,
    carrinho_routes,
    item_carrinho_routes,
    dashboard_routes,
    aplicacao_vacina_routes,
    vacina_routes
    
)

from contextlib import asynccontextmanager
from backend.database.database import create_db_and_tables
@asynccontextmanager

async def lifespan(app: FastAPI):
    create_db_and_tables()
    criar_admin()

    yield



app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)

app.include_router(cadastro_routes.router)
app.include_router(login_routes.router)
app.include_router(logout_routes.router)
app.include_router(usuario_routes.router)
app.include_router(cliente_routes.router)
app.include_router(animal_routes.router)
app.include_router(agendamento_routes.router)
app.include_router(atendimento_routes.router)
app.include_router(produto_routes.router)
app.include_router(carrinho_routes.router)
app.include_router(item_carrinho_routes.router)
app.include_router(dashboard_routes.router)
app.include_router(aplicacao_vacina_routes.router)
app.include_router(vacina_routes.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )