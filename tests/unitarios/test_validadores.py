import re
import pytest

def normalizar_cpf(valor):
    return re.sub(r"\D", "", valor or "")

def cpf_formato_valido(valor):
    return bool(re.fullmatch(r"\d{11}", normalizar_cpf(valor)))

@pytest.mark.unitario
@pytest.mark.parametrize("cpf", ["529.982.247-25", "52998224725"])
def test_normalizacao_de_cpf_remove_mascara(cpf):
    assert cpf_formato_valido(cpf)

@pytest.mark.unitario
@pytest.mark.parametrize("cpf", ["", "123", "abcdefghijk", None, "123456789012"])
def test_cpf_com_quantidade_ou_conteudo_invalido(cpf):
    assert not cpf_formato_valido(cpf)

@pytest.mark.unitario
@pytest.mark.parametrize("texto, esperado", [
    ("  Rex  ", "Rex"), ("", ""), ("   ", ""), (None, "")
])
def test_normalizacao_de_texto_basica(texto, esperado):
    resultado = texto.strip() if isinstance(texto, str) else ""
    assert resultado == esperado
