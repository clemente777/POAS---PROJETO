from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware

from backend.database.database import create_db_and_tables
from backend.database.seed import (
    criar_admin,
    criar_produtos_teste,
)
from backend.exceptions.handlers import tratar_validacao
from backend.models import *
from backend.routes import (
    agendamento_routes,
    animal_routes,
    aplicacao_vacina_routes,
    atendimento_routes,
    cadastro_routes,
    carrinho_routes,
    cliente_routes,
    dashboard_routes,
    item_carrinho_routes,
    login_routes,
    logout_routes,
    pedido_routes,
    produto_routes,
    usuario_routes,
    vacina_routes,
)


@asynccontextmanager

async def lifespan(app: FastAPI):
    create_db_and_tables()
    criar_admin()
    criar_produtos_teste()

    yield


app = FastAPI(lifespan=lifespan)

app.add_exception_handler(
    RequestValidationError,
    tratar_validacao
)
app.add_middleware(
    CORSMiddleware,

    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://10.144.8.227:5173",
        # Aplicativo PWA em ambiente de produção local.
        "http://localhost:4173",
        "http://127.0.0.1:4173",
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
app.include_router(pedido_routes.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
