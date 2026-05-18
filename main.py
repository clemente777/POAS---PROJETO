from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/", response_class=HTMLResponse)
def home():

    with open("templates/index.html", "r", encoding="utf-8") as arquivo:
        html = arquivo.read()

    return HTMLResponse(content=html)


@app.post("/register")
def register():

    return {
        "mensagem": "Usuário cadastrado"
    }


@app.post("/login")
def login():

    return {
        "mensagem": "Login realizado"
    }


@app.get("/produtos")
def produtos():

    return {
        "produtos": []
    }