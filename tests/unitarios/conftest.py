from types import SimpleNamespace
from unittest.mock import MagicMock
import pytest

@pytest.fixture
def repositorio_mock():
    return MagicMock()

@pytest.fixture
def usuario_admin():
    return SimpleNamespace(id=1, perfil="Administrador", email="admin@teste.local")

@pytest.fixture
def usuario_veterinario():
    return SimpleNamespace(id=2, perfil="Veterinário", email="vet@teste.local")

@pytest.fixture
def usuario_cliente():
    return SimpleNamespace(id=3, perfil="Cliente", email="cliente@teste.local")
