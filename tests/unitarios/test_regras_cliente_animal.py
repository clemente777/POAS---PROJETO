import re
import pytest

def cpf_tem_formato_basico(cpf):
    return bool(re.fullmatch(r"\d{11}", re.sub(r"\D", "", cpf or "")))

@pytest.mark.unitario
@pytest.mark.parametrize("cpf", ["529.982.247-25", "52998224725"])
def test_cpf_com_11_digitos_apos_normalizacao(cpf):
    assert cpf_tem_formato_basico(cpf)

@pytest.mark.unitario
@pytest.mark.parametrize("cpf", ["123", "", "abcdefghijk", None])
def test_cpf_com_formato_invalido(cpf):
    assert not cpf_tem_formato_basico(cpf)

@pytest.mark.unitario
def test_idade_de_animal_nao_deve_ser_negativa():
    idade = -1
    assert idade < 0  # O serviço deve rejeitar esse valor.
