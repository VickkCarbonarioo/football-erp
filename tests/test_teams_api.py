
# Verifica se uma equipe é cadastrada corretamente pela API.
def test_create_team_returns_created_team(client):
    # Cadastra um clube para vincular à equipe.
    club_response = client.post(
        "/clubs",
        json={"name": "Santos"},
    )

    # Obtém o ID do clube criado.
    club_id = club_response.json()["id"]

    # Envia os dados da equipe para a API.
    response = client.post(
        "/teams",
        json={
            "name": "Sub-17 Santos",
            "category": "Base",
            "gender": "Masculino",
            "age_group": "Sub-17",
            "club_id": club_id,
        },
    )

    # Confirma que a equipe foi criada.
    assert response.status_code == 201

    # Obtém os dados retornados pela API.
    team = response.json()

    # Confirma os dados principais da equipe.
    assert team["name"] == "Sub-17 Santos"
    assert team["category"] == "Base"
    assert team["gender"] == "Masculino"
    assert team["age_group"] == "Sub-17"
    assert team["club_id"] == club_id

    # Confirma o status padrão e o ID gerado.
    assert team["status"] == "active"
    assert team["id"] is not None

    # Confirma que as datas foram retornadas.
    assert team["created_at"] is not None
    assert team["updated_at"] is not None


# Verifica se o cadastro rejeita um clube inexistente.
def test_create_team_with_nonexistent_club_returns_not_found(client):
    # Tenta cadastrar uma equipe vinculada a um clube inexistente.
    response = client.post(
        "/teams",
        json={
            "name": "Sub-20",
            "category": "Base",
            "gender": "Masculino",
            "age_group": "Sub-20",
            "club_id": 99999,
        },
    )

    # Confirma o código de clube não encontrado.
    assert response.status_code == 404

    # Confirma a mensagem retornada.
    assert response.json()["detail"] == "Clube não encontrado."


# Verifica se a API lista as equipes de um clube.
def test_list_teams_by_club_returns_all_teams(client):
    # Cadastra um clube.
    club_response = client.post(
        "/clubs",
        json={"name": "Santos"},
    )
    club_id = club_response.json()["id"]

    # Cadastra a primeira equipe.
    client.post(
        "/teams",
        json={
            "name": "Sub-17 Santos",
            "category": "Base",
            "gender": "Masculino",
            "age_group": "Sub-17",
            "club_id": club_id,
        },
    )

    # Cadastra a segunda equipe.
    client.post(
        "/teams",
        json={
            "name": "Sub-20 Santos",
            "category": "Base",
            "gender": "Masculino",
            "age_group": "Sub-20",
            "club_id": club_id,
        },
    )

    # Consulta as equipes do clube.
    response = client.get(f"/clubs/{club_id}/teams")

    # Confirma que a consulta funcionou.
    assert response.status_code == 200

    # Obtém as equipes retornadas pela API.
    teams = response.json()

    # Confirma que as duas equipes foram encontradas.
    assert len(teams) == 2

    # Confirma os nomes das equipes.
    assert {team["name"] for team in teams} == {
        "Sub-17 Santos",
        "Sub-20 Santos",
    }

    # Confirma que ambas pertencem ao clube consultado.
    assert all(
        team["club_id"] == club_id
        for team in teams
    )


# Verifica se a API rejeita a consulta de um clube inexistente.
def test_list_teams_by_nonexistent_club_returns_not_found(client):
    # Consulta as equipes de um clube inexistente.
    response = client.get("/clubs/99999/teams")

    # Confirma o código de clube não encontrado.
    assert response.status_code == 404

    # Confirma a mensagem retornada.
    assert response.json()["detail"] == "Clube não encontrado."


# Verifica se a API não mistura equipes de clubes diferentes.
def test_list_teams_by_club_does_not_mix_clubs(client):
    # Cadastra o Santos.
    santos_response = client.post(
        "/clubs",
        json={"name": "Santos"},
    )
    santos_id = santos_response.json()["id"]

    # Cadastra o Palmeiras.
    palmeiras_response = client.post(
        "/clubs",
        json={"name": "Palmeiras"},
    )
    palmeiras_id = palmeiras_response.json()["id"]

    # Cadastra uma equipe no Santos.
    client.post(
        "/teams",
        json={
            "name": "Sub-17 Santos",
            "category": "Base",
            "gender": "Masculino",
            "age_group": "Sub-17",
            "club_id": santos_id,
        },
    )

    # Cadastra uma equipe no Palmeiras.
    client.post(
        "/teams",
        json={
            "name": "Sub-20 Palmeiras",
            "category": "Base",
            "gender": "Masculino",
            "age_group": "Sub-20",
            "club_id": palmeiras_id,
        },
    )

    # Consulta somente as equipes do Santos.
    response = client.get(f"/clubs/{santos_id}/teams")

    # Confirma que a consulta funcionou.
    assert response.status_code == 200

    # Confirma que somente a equipe do Santos foi retornada.
    teams = response.json()
    assert len(teams) == 1
    assert teams[0]["name"] == "Sub-17 Santos"
    assert teams[0]["club_id"] == santos_id
