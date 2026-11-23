import os
import pytest

@pytest.mark.funcional
def test_fluxo_login_e_token(api_url, sessao_http):
    email = os.getenv("POAS_TEST_EMAIL")
    senha = os.getenv("POAS_TEST_PASSWORD")
    if not email or not senha:
        pytest.skip("Configure POAS_TEST_EMAIL e POAS_TEST_PASSWORD para uma conta de teste.")
    r = sessao_http.post(
        f"{api_url}/login/",
        data={"username": email, "password": senha},
        timeout=10,
    )
    assert r.status_code == 200, r.text
    body = r.json()
    assert body.get("access_token")
    assert body.get("token_type", "bearer").lower() == "bearer"
