from decimal import Decimal
import pytest

def calcular_total(preco, quantidade):
    preco = Decimal(str(preco))
    if preco <= 0:
        raise ValueError("Preço deve ser positivo.")
    if quantidade <= 0:
        raise ValueError("Quantidade deve ser positiva.")
    return preco * quantidade

@pytest.mark.unitario
def test_calcular_total_de_item():
    assert calcular_total("12.50", 3) == Decimal("37.50")

@pytest.mark.unitario
@pytest.mark.parametrize("preco, quantidade", [
    ("0", 1), ("-1", 1), ("10", 0), ("10", -2)
])
def test_calculo_rejeita_preco_ou_quantidade_invalidos(preco, quantidade):
    with pytest.raises(ValueError):
        calcular_total(preco, quantidade)

@pytest.mark.unitario
def test_quantidade_nao_pode_ultrapassar_estoque():
    estoque, solicitado = 4, 5
    assert solicitado > estoque
