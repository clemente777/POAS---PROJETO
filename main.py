from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")



@app.get("/", response_class=HTMLResponse)
def home():
    with open("templates/index.html", "r", encoding="utf-8") as arquivo:
        return HTMLResponse(content=arquivo.read())



@app.get("/login-page", response_class=HTMLResponse)
def login_page():
    with open("templates/login.html", "r", encoding="utf-8") as arquivo:
        return HTMLResponse(content=arquivo.read())



@app.post("/login")
async def login(request: Request):
    data = await request.json()

    usuario = data.get("usuario")
    senha = data.get("senha")

    if usuario == "admin" and senha == "123":
        return {"mensagem": "Login realizado com sucesso"}
    
    return {"mensagem": "Usuário ou senha inválidos"}


@app.post("/register")
def register():
    return {"mensagem": "Usuário cadastrado"}


@app.get("/produtos")
def produtos():
    return {"produtos": []}