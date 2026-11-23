import pytest
import requests

@pytest.mark.funcional
@pytest.mark.parametrize("modulo", [
    "animais", "agendamentos", "atendimentos", "vacinas",
    "aplicacoes-vacina", "produtos", "carrinho", "dashboard",
])
def test_modulo_exposto_pela_api(api_url, modulo):
    spec = requests.get(f"{api_url}/openapi.json", timeout=10).json()
    caminhos = [p for p in spec.get("paths", {}) if modulo in p.lower().replace("_", "-")]
    assert caminhos, f"Nenhuma rota do módulo '{modulo}' foi encontrada no OpenAPI."
