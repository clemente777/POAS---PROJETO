
from fastapi import FastAPI
from backend.routes import usuario_routes, login_router

app = FastAPI()

app.include_router(usuario_routes.router)
app.include_router(login_router.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
