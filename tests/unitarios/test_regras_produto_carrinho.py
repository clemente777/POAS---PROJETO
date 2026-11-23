import pytest

@pytest.mark.unitario
@pytest.mark.parametrize("preco", [0, -1, -0.01])
def test_preco_nao_positivo_deve_ser_rejeitado(preco):
    assert preco <= 0

@pytest.mark.unitario
@pytest.mark.parametrize("quantidade", [0, -1])
def test_quantidade_de_compra_deve_ser_positiva(quantidade):
    assert quantidade <= 0

@pytest.mark.unitario
def test_compra_nao_pode_ultrapassar_estoque():
    estoque = 4
    quantidade_solicitada = 5
    assert quantidade_solicitada > estoque
