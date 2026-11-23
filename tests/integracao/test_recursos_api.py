import pytest

MODULOS_ESPERADOS = [
    "usuarios", "clientes", "animais", "agendamentos", "atendimentos",
    "vacinas", "aplicacoes-vacina", "produtos", "carrinho",
]

@pytest.mark.integracao
@pytest.mark.parametrize("modulo", MODULOS_ESPERADOS)
def test_modulo_possui_rota_documentada(openapi, modulo):
    paths = list(openapi.get("paths", {}))
    normalizados = [(p, p.lower().replace("_", "-")) for p in paths]
    assert any(modulo in normalizado for _, normalizado in normalizados), (
        f"Módulo '{modulo}' não encontrado no OpenAPI. Rotas documentadas: {paths}"
    )

@pytest.mark.integracao
def test_login_esta_documentado(openapi):
    assert any("login" in p.lower() for p in openapi.get("paths", {}))

@pytest.mark.integracao
def test_rotas_de_escrita_documentam_respostas(openapi):
    metodos_escrita = {"post", "put", "patch", "delete"}
    for path, operacoes in openapi.get("paths", {}).items():
        for metodo in metodos_escrita.intersection(operacoes):
            respostas = operacoes[metodo].get("responses", {})
            assert respostas, f"{metodo.upper()} {path} não documenta respostas."
