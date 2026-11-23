import pytest

@pytest.mark.integracao
def test_api_responde_com_openapi(openapi):
    assert isinstance(openapi, dict)
    assert openapi.get("openapi")
    assert isinstance(openapi.get("paths"), dict)
    assert openapi["paths"], "OpenAPI foi carregado, mas não documenta nenhuma rota."

@pytest.mark.integracao
@pytest.mark.parametrize("termo", ["login", "animal", "agendamento", "produto"])
def test_openapi_documenta_modulos_essenciais(openapi, termo):
    paths = list(openapi.get("paths", {}))
    encontrados = [p for p in paths if termo in p.lower()]
    assert encontrados, f"Nenhuma rota contendo '{termo}' foi encontrada. Rotas: {paths}"

@pytest.mark.integracao
def test_openapi_documenta_metodos_http_validos(openapi):
    metodos = {"get", "post", "put", "patch", "delete"}
    for path, operacoes in openapi["paths"].items():
        assert isinstance(operacoes, dict), f"Definição inválida para {path}"
        assert any(m in metodos for m in operacoes), (
            f"A rota {path} não possui método HTTP documentado."
        )
