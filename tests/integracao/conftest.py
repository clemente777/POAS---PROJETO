import uuid
import pytest
import requests

@pytest.fixture
def http():
    s = requests.Session()
    s.headers.update({"Accept": "application/json"})
    yield s
    s.close()

@pytest.fixture
def email_unico():
    return f"teste_{uuid.uuid4().hex[:12]}@example.test"
