
# Verifica se um jogador é cadastrado corretamente pela API.
def test_create_player_returns_created_player(client):
    # Cadastra um clube para servir de base à equipe.
    club_response = client.post(
        "/clubs",
        json={"name": "Santos"},
    )
    club_id = club_response.json()["id"]

    # Cadastra a equipe à qual o jogador será vinculado.
    team_response = client.post(
        "/teams",
        json={
            "name": "Sub-17 Santos",
            "category": "Base",
            "gender": "Masculino",
            "age_group": "Sub-17",
            "club_id": club_id,
        },
    )
    team_id = team_response.json()["id"]

    # Envia os dados do jogador para a API.
    response = client.post(
        "/players",
        json={
            "name": "João Silva",
            "birth_date": "2005-04-15",
            "nationality": "Brazilian",
            "dominant_foot": "right",
            "height_cm": 180,
            "shirt_number": 9,
            "team_id": team_id,
        },
    )

    # Confirma que o jogador foi cadastrado.
    assert response.status_code == 201

    # Obtém os dados retornados pela API.
    player = response.json()

    # Confirma os dados principais do jogador.
    assert player["name"] == "João Silva"
    assert player["birth_date"] == "2005-04-15"
    assert player["nationality"] == "Brazilian"
    assert player["dominant_foot"] == "right"
    assert player["height_cm"] == 180
    assert player["shirt_number"] == 9
    assert player["team_id"] == team_id

    # Confirma o status padrão e o ID gerado.
    assert player["status"] == "active"
    assert player["id"] is not None

    # Confirma que as datas foram retornadas.
    assert player["created_at"] is not None
    assert player["updated_at"] is not None


# Verifica se o cadastro rejeita uma equipe inexistente.
def test_create_player_with_nonexistent_team_returns_not_found(client):
    # Tenta cadastrar um jogador em uma equipe inexistente.
    response = client.post(
        "/players",
        json={
            "name": "João Silva",
            "birth_date": "2005-04-15",
            "nationality": "Brazilian",
            "dominant_foot": "right",
            "height_cm": 180,
            "shirt_number": 9,
            "team_id": 99999,
        },
    )

    # Confirma o código de equipe não encontrada.
    assert response.status_code == 404

    # Confirma a mensagem retornada.
    assert response.json()["detail"] == "Equipe não encontrada."


# Verifica se a API lista os jogadores de uma equipe.
def test_list_players_by_team_returns_players(client):
    # Cadastra um clube.
    club_response = client.post(
        "/clubs",
        json={"name": "Santos"},
    )
    club_id = club_response.json()["id"]

    # Cadastra a equipe.
    team_response = client.post(
        "/teams",
        json={
            "name": "Sub-17 Santos",
            "category": "Base",
            "gender": "Masculino",
            "age_group": "Sub-17",
            "club_id": club_id,
        },
    )
    team_id = team_response.json()["id"]

    # Cadastra o primeiro jogador.
    client.post(
        "/players",
        json={
            "name": "João Silva",
            "birth_date": "2005-04-15",
            "nationality": "Brazilian",
            "dominant_foot": "right",
            "height_cm": 180,
            "shirt_number": 9,
            "team_id": team_id,
        },
    )

    # Cadastra o segundo jogador.
    client.post(
        "/players",
        json={
            "name": "Pedro Santos",
            "birth_date": "2006-08-20",
            "nationality": "Brazilian",
            "dominant_foot": "left",
            "height_cm": 175,
            "shirt_number": 10,
            "team_id": team_id,
        },
    )

    # Consulta os jogadores da equipe.
    response = client.get(f"/teams/{team_id}/players")

    # Confirma que a consulta funcionou.
    assert response.status_code == 200

    # Obtém os jogadores retornados pela API.
    players = response.json()

    # Confirma que os dois jogadores foram encontrados.
    assert len(players) == 2

    # Confirma os nomes dos jogadores.
    assert {player["name"] for player in players} == {
        "João Silva",
        "Pedro Santos",
    }

    # Confirma que ambos pertencem à equipe consultada.
    assert all(
        player["team_id"] == team_id
        for player in players
    )


# Verifica se a listagem rejeita uma equipe inexistente.
def test_list_players_by_nonexistent_team_returns_not_found(client):
    # Consulta os jogadores de uma equipe inexistente.
    response = client.get("/teams/99999/players")

    # Confirma o código de equipe não encontrada.
    assert response.status_code == 404

    # Confirma a mensagem retornada.
    assert response.json()["detail"] == "Equipe não encontrada."

# Verifica se uma equipe sem jogadores retorna uma lista vazia.
def test_list_players_by_team_returns_empty_list(client):
    # Cadastra um clube para servir de base à equipe.
    club_response = client.post(
        "/clubs",
        json={"name": "Corinthians"},
    )
    club_id = club_response.json()["id"]

    # Cadastra uma equipe sem jogadores.
    team_response = client.post(
        "/teams",
        json={
            "name": "Sub-17 Corinthians",
            "category": "Base",
            "gender": "Masculino",
            "age_group": "Sub-17",
            "club_id": club_id,
        },
    )
    team_id = team_response.json()["id"]

    # Consulta os jogadores da equipe recém-criada.
    response = client.get(f"/teams/{team_id}/players")

    # Confirma que a consulta foi realizada com sucesso.
    assert response.status_code == 200

    # Confirma que nenhum jogador foi encontrado.
    assert response.json() == []
