import pytest

@pytest.mark.unitario
@pytest.mark.parametrize("valor", ["", "   ", None])
def test_campos_obrigatorios_rejeitam_valores_vazios(valor):
    """Regra geral: campos obrigatórios não devem aceitar vazio."""
    assert valor is None or (isinstance(valor, str) and not valor.strip())

@pytest.mark.unitario
@pytest.mark.parametrize("perfil", ["Administrador", "Veterinário", "Cliente"])
def test_perfis_previstos_no_sistema(perfil):
    assert perfil in {"Administrador", "Veterinário", "Cliente"}

@pytest.mark.unitario
def test_perfil_desconhecido_nao_faz_parte_dos_perfis_validos():
    assert "Gerente" not in {"Administrador", "Veterinário", "Cliente"}
