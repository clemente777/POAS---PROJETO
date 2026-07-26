from datetime import date, timedelta


def test_dashboard_completo(client, auth_headers):

    response = client.get(
        "/dashboard/",
        headers=auth_headers
    )

    assert response.status_code == 200

    data = response.json()


    # =========================
    # Totais do sistema
    # =========================

    assert "usuarios" in data
    assert "clientes" in data
    assert "animais" in data
    assert "agendamentos" in data
    assert "atendimentos" in data
    assert "produtos" in data
    assert "carrinhos" in data
    assert "itens_carrinho" in data


    assert isinstance(
        data["usuarios"],
        int
    )

    assert isinstance(
        data["clientes"],
        int
    )


    # =========================
    # Estoque
    # =========================

    assert "valor_total_estoque" in data

    assert data["valor_total_estoque"] >= 0


    assert "estoque_baixo" in data

    assert data["estoque_baixo"] >= 0


    assert "produtos_sem_estoque" in data

    assert data["produtos_sem_estoque"] >= 0



    # =========================
    # Produtos
    # =========================

    assert "produto_mais_caro" in data

    if data["produto_mais_caro"]:

        assert "nome" in data["produto_mais_caro"]

        assert "preco" in data["produto_mais_caro"]



    assert "produto_mais_barato" in data

    if data["produto_mais_barato"]:

        assert "nome" in data["produto_mais_barato"]

        assert "preco" in data["produto_mais_barato"]



    # =========================
    # Animais
    # =========================

    assert "animal_mais_velho" in data

    if data["animal_mais_velho"]:

        assert "nome" in data["animal_mais_velho"]

        assert "idade" in data["animal_mais_velho"]


    assert "media_idade_animais" in data

    assert data["media_idade_animais"] >= 0



    # =========================
    # Clientes
    # =========================

    assert "cliente_com_mais_animais" in data


    if data["cliente_com_mais_animais"]:

        assert "nome" in data["cliente_com_mais_animais"]

        assert (
            "quantidade"
            in data["cliente_com_mais_animais"]
        )



    # =========================
    # Agenda
    # =========================

    assert "agendamentos_hoje" in data

    assert (
        data["agendamentos_hoje"]
        >= 0
    )


    assert "agendamentos_futuros" in data

    assert (
        data["agendamentos_futuros"]
        >= 0
    )