
# Importa date para montar datas nos testes de encerramento.
from datetime import date

# Define os dados válidos que usaremos nos testes de contratos.
contract_data = {
    "start_date": "2026-01-01",
    "end_date": "2026-12-31",
    "monthly_salary": "15000.00",
    "total_value": "180000.00",
}


# Cria um clube, uma equipe e um jogador para os testes.
def create_test_player(client):
    # Cadastra um clube para vincular à equipe.
    club_response = client.post(
        "/clubs",
        json={"name": "Clube de Teste"},
    )

    # Confirma que o clube foi criado.
    assert club_response.status_code == 201

    # Obtém o ID do clube criado.
    club_id = club_response.json()["id"]

    # Cadastra uma equipe para vincular ao jogador.
    team_response = client.post(
        "/teams",
        json={
            "name": "Equipe Sub-20",
            "category": "Base",
            "gender": "Masculino",
            "age_group": "Sub-20",
            "club_id": club_id,
        },
    )

    # Confirma que a equipe foi criada.
    assert team_response.status_code == 201

    # Obtém o ID da equipe criada.
    team_id = team_response.json()["id"]

    # Cadastra um jogador para receber o contrato.
    player_response = client.post(
        "/players",
        json={
            "name": "Jogador de Teste",
            "birth_date": "2005-05-10",
            "nationality": "Brasileira",
            "dominant_foot": "right",
            "height_cm": 180,
            "shirt_number": 10,
            "team_id": team_id,
        },
    )

    # Confirma que o jogador foi criado.
    assert player_response.status_code == 201

    # Retorna o ID do jogador criado.
    return player_response.json()["id"]


# Cria um contrato pela API e retorna sua resposta.
def create_test_contract(client, player_id, extra_data=None):
    # Monta os dados do contrato.
    payload = {
        **contract_data,
        "player_id": player_id,
    }

    # Permite personalizar os dados de cada teste.
    if extra_data:
        payload.update(extra_data)

    # Envia a requisição para cadastrar o contrato.
    return client.post("/contracts", json=payload)


# Testa o cadastro de um contrato válido.
def test_create_contract_returns_created_contract(client):
    # Cria um jogador para receber o contrato.
    player_id = create_test_player(client)

    # Cadastra o contrato.
    response = create_test_contract(client, player_id)

    # Verifica se o contrato foi criado.
    assert response.status_code == 201

    # Confirma que o contrato pertence ao jogador correto.
    assert response.json()["player_id"] == player_id

    # Confirma o salário com duas casas decimais.
    assert response.json()["monthly_salary"] == "15000.00"

    # Confirma o valor total com duas casas decimais.
    assert response.json()["total_value"] == "180000.00"


# Testa o cadastro para um jogador inexistente.
def test_create_contract_with_nonexistent_player_returns_not_found(client):
    # Tenta cadastrar um contrato usando um ID inexistente.
    response = create_test_contract(client, 99999)

    # Confirma que a API informou que o jogador não existe.
    assert response.status_code == 404
    assert response.json()["detail"] == "Jogador não encontrado."


# Testa a listagem do histórico de contratos.
def test_list_contracts_by_player_returns_contracts(client):
    # Cria um jogador para receber o contrato.
    player_id = create_test_player(client)

    # Cadastra um contrato.
    create_response = create_test_contract(client, player_id)

    # Confirma que o cadastro foi bem-sucedido.
    assert create_response.status_code == 201

    # Consulta o histórico do jogador.
    response = client.get(f"/players/{player_id}/contracts")

    # Verifica se a consulta foi bem-sucedida.
    assert response.status_code == 200

    # Confirma que o histórico contém um contrato.
    assert len(response.json()) == 1
    assert response.json()[0]["player_id"] == player_id


# Testa se dois contratos são preservados no histórico.
def test_contract_history_preserves_multiple_contracts(client):
    # Cria um jogador para receber os contratos.
    player_id = create_test_player(client)

    # Cadastra o primeiro contrato.
    first_response = create_test_contract(client, player_id)

    # Cadastra um segundo contrato com outro período.
    second_response = create_test_contract(
        client,
        player_id,
        {
            "start_date": "2027-01-01",
            "end_date": "2027-12-31",
            "monthly_salary": "18000.00",
            "total_value": "216000.00",
        },
    )

    # Confirma que ambos os contratos foram criados.
    assert first_response.status_code == 201
    assert second_response.status_code == 201

    # Consulta o histórico completo.
    history_response = client.get(
        f"/players/{player_id}/contracts"
    )

    # Confirma que nenhum contrato anterior foi apagado.
    assert history_response.status_code == 200
    assert len(history_response.json()) == 2


# Testa o histórico de um jogador que ainda não possui contratos.
def test_list_contracts_for_player_without_contracts_returns_empty_list(client):
    # Cria um jogador sem cadastrar nenhum contrato.
    player_id = create_test_player(client)

    # Consulta o histórico do jogador.
    response = client.get(f"/players/{player_id}/contracts")

    # A consulta deve funcionar e retornar uma lista vazia.
    assert response.status_code == 200
    assert response.json() == []


# Testa a consulta do histórico de um jogador inexistente.
def test_list_contracts_for_nonexistent_player_returns_not_found(client):
    # Consulta um ID de jogador inexistente.
    response = client.get("/players/99999/contracts")

    # Confirma que a API informa que o jogador não existe.
    assert response.status_code == 404
    assert response.json()["detail"] == "Jogador não encontrado."


# Testa a rejeição de um contrato com datas inválidas.
def test_create_contract_with_invalid_dates_returns_unprocessable_entity(client):
    # Cria um jogador para o teste.
    player_id = create_test_player(client)

    # Tenta cadastrar um contrato cuja data final vem antes da inicial.
    response = create_test_contract(
        client,
        player_id,
        {
            "start_date": "2026-12-31",
            "end_date": "2026-01-01",
        },
    )

    # Confirma que a validação rejeitou as datas.
    assert response.status_code == 422


# Testa a rejeição de um salário negativo.
def test_create_contract_with_negative_salary_returns_unprocessable_entity(client):
    # Cria um jogador para o teste.
    player_id = create_test_player(client)

    # Tenta cadastrar um contrato com salário negativo.
    response = create_test_contract(
        client,
        player_id,
        {"monthly_salary": "-100.00"},
    )

    # Confirma que a validação rejeitou o salário.
    assert response.status_code == 422


# Testa o encerramento antecipado de um contrato.
def test_terminate_contract_returns_updated_contract(client):
    # Cria um jogador e seu contrato.
    player_id = create_test_player(client)
    create_response = create_test_contract(client, player_id)

    # Confirma que o contrato foi criado.
    assert create_response.status_code == 201

    # Obtém o ID do contrato criado.
    contract_id = create_response.json()["id"]

    # Envia a data de encerramento antecipado.
    response = client.post(
        f"/contracts/{contract_id}/terminate",
        params={"terminated_at": "2026-06-30"},
    )

    # Confirma que o encerramento foi aceito.
    assert response.status_code == 200
    assert response.json()["terminated_at"] == "2026-06-30"


# Testa a rejeição de um segundo encerramento.
def test_terminate_contract_twice_returns_conflict(client):
    # Cria um jogador e seu contrato.
    player_id = create_test_player(client)
    create_response = create_test_contract(client, player_id)

    # Obtém o ID do contrato criado.
    contract_id = create_response.json()["id"]

    # Encerra o contrato pela primeira vez.
    first_response = client.post(
        f"/contracts/{contract_id}/terminate",
        params={"terminated_at": "2026-06-30"},
    )

    # Tenta encerrar o mesmo contrato novamente.
    second_response = client.post(
        f"/contracts/{contract_id}/terminate",
        params={"terminated_at": "2026-07-01"},
    )

    # Confirma o sucesso da primeira operação.
    assert first_response.status_code == 200

    # Confirma que a segunda operação foi rejeitada.
    assert second_response.status_code == 409


# Testa uma data de encerramento anterior ao início do contrato.
def test_terminate_contract_before_start_returns_conflict(client):
    # Cria um jogador e seu contrato.
    player_id = create_test_player(client)
    create_response = create_test_contract(client, player_id)

    # Obtém o ID do contrato criado.
    contract_id = create_response.json()["id"]

    # Tenta encerrar o contrato antes de seu início.
    response = client.post(
        f"/contracts/{contract_id}/terminate",
        params={"terminated_at": "2025-12-31"},
    )

    # Confirma que a data inválida foi rejeitada.
    assert response.status_code == 409


# Testa a rejeição de uma data posterior ao fim previsto.
def test_terminate_contract_after_end_returns_conflict(client):
    # Cria um jogador e seu contrato.
    player_id = create_test_player(client)
    create_response = create_test_contract(client, player_id)

    # Obtém o ID do contrato criado.
    contract_id = create_response.json()["id"]

    # Tenta encerrar o contrato depois do fim previsto.
    response = client.post(
        f"/contracts/{contract_id}/terminate",
        params={"terminated_at": "2027-01-01"},
    )

    # Confirma que a data inválida foi rejeitada.
    assert response.status_code == 409


# Testa a tentativa de encerrar um contrato inexistente.
def test_terminate_nonexistent_contract_returns_not_found(client):
    # Tenta encerrar um contrato que não existe.
    response = client.post(
        "/contracts/99999/terminate",
        params={"terminated_at": "2026-06-30"},
    )

    # Confirma que a API informou que o contrato não existe.
    assert response.status_code == 404
