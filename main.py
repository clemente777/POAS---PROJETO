from fastapi import FastAPI
from backend.models import *

from backend.routes import (
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
    
)

from contextlib import asynccontextmanager
from backend.database.database import create_db_and_tables

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield



app = FastAPI(lifespan=lifespan)



app.include_router(usuario_routes.router)
app.include_router(login_routes.router)
app.include_router(logout_routes.router)
app.include_router(cliente_routes.router)
app.include_router(animal_routes.router)
app.include_router(agendamento_routes.router)
app.include_router(atendimento_routes.router)
app.include_router(produto_routes.router)
app.include_router(carrinho_routes.router)
app.include_router(item_carrinho_routes.router)
app.include_router(dashboard_routes.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )