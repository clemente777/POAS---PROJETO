
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.database.database import create_db_and_tables
from backend.database.seed import (
    criar_admin,
    criar_produtos_teste,
)
from backend.models import *
from backend.routes import (
    cadastro_routes,
    pedido_routes,
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
    vacina_routes,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    criar_admin()
    criar_produtos_teste()

    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://10.145.6.7:5173"
    ],
    # Libera o front-end aberto pelo IP da rede local.
    allow_origin_regex=(
        r"^http://(192\.168\.\d+\.\d+|10\.\d+\.\d+\.\d+|172\."
        r"(1[6-9]|2\d|3[01])\.\d+\.\d+):5173$"
    ),
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
        reload=True,
    )
