from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError



async def tratar_validacao(
    request: Request,
    exc: RequestValidationError
):

    erros = []


    for erro in exc.errors():

        campo = ".".join(
            str(item)
            for item in erro["loc"]
            if item != "body"
        )


        tipo = erro["type"]


        mensagem = "Dados inválidos."



        if tipo == "missing":

            mensagem = (
                f"O campo '{campo}' é obrigatório."
            )


        elif tipo in [
            "value_error.email",
            "value_error"
        ]:

            mensagem = (
                "Email inválido. "
                "Digite um email válido."
            )


        elif tipo == "string_too_short":

            mensagem = (
                f"O campo '{campo}' "
                "possui poucos caracteres."
            )


        elif tipo == "string_too_long":

            mensagem = (
                f"O campo '{campo}' "
                "possui muitos caracteres."
            )


        elif tipo == "int_parsing":

            mensagem = (
                f"O campo '{campo}' "
                "deve ser um número."
            )


        erros.append(
            {
                "campo": campo,
                "mensagem": mensagem
            }
        )


    return JSONResponse(

        status_code=422,

        content={
            "detail": erros
        }

    )