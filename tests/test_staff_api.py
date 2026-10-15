
def test_create_staff_member_returns_created_staff_member(client):
    # Cadastra um clube para vincular o profissional.
    club_response = client.post(
        "/clubs",
        json={"name": "Santos"},
    )

    # Obtém o ID do clube criado.
    club_id = club_response.json()["id"]

    # Envia os dados do profissional para a API.
    response = client.post(
        "/staff",
        json={
            "name": "Ana Silva",
            "role": "Preparadora física",
            "club_id": club_id,
        },
    )

    # Verifica se o profissional foi criado.
    assert response.status_code == 201

    # Confirma os dados retornados pela API.
    assert response.json()["name"] == "Ana Silva"
    assert response.json()["role"] == "Preparadora física"
    assert response.json()["club_id"] == club_id

    # Verifica se o profissional recebeu um ID.
    assert response.json()["id"] is not None


def test_create_staff_member_with_nonexistent_club_returns_not_found(client):
    # Tenta cadastrar um profissional vinculado a um clube inexistente.
    response = client.post(
        "/staff",
        json={
            "name": "Ana Silva",
            "role": "Preparadora física",
            "club_id": 99999,
        },
    )

    # Confirma que a API informa que o clube não foi encontrado.
    assert response.status_code == 404

    # Confirma a mensagem de erro retornada.
    assert response.json()["detail"] == "Clube não encontrado."


def test_list_staff_members_by_club_returns_all_members(client):
    # Cadastra um clube para os profissionais.
    club_response = client.post(
        "/clubs",
        json={"name": "Santos"},
    )

    # Obtém o ID do clube criado.
    club_id = club_response.json()["id"]

    # Cadastra a primeira profissional.
    client.post(
        "/staff",
        json={
            "name": "Ana Silva",
            "role": "Preparadora física",
            "club_id": club_id,
        },
    )

    # Cadastra o segundo profissional.
    client.post(
        "/staff",
        json={
            "name": "Carlos Souza",
            "role": "Auxiliar técnico",
            "club_id": club_id,
        },
    )

    # Consulta a comissão técnica do clube.
    response = client.get(f"/clubs/{club_id}/staff")

    # Confirma que a consulta foi bem-sucedida.
    assert response.status_code == 200

    # Obtém a lista retornada pela API.
    staff_members = response.json()

    # Confirma que os dois profissionais foram encontrados.
    assert len(staff_members) == 2

    # Confirma os nomes dos profissionais retornados.
    assert {member["name"] for member in staff_members} == {
        "Ana Silva",
        "Carlos Souza",
    }

    # Confirma que todos pertencem ao clube consultado.
    assert all(
        member["club_id"] == club_id
        for member in staff_members
    )


def test_list_staff_members_by_nonexistent_club_returns_not_found(client):
    # Consulta a comissão técnica de um clube inexistente.
    response = client.get("/clubs/99999/staff")

    # Confirma que a API informa que o clube não foi encontrado.
    assert response.status_code == 404

    # Confirma a mensagem de erro retornada.
    assert response.json()["detail"] == "Clube não encontrado."


def test_list_staff_members_by_club_does_not_mix_clubs(client):
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

    # Cadastra um profissional no Santos.
    client.post(
        "/staff",
        json={
            "name": "Ana Silva",
            "role": "Preparadora física",
            "club_id": santos_id,
        },
    )

    # Cadastra um profissional no Palmeiras.
    client.post(
        "/staff",
        json={
            "name": "Carlos Souza",
            "role": "Auxiliar técnico",
            "club_id": palmeiras_id,
        },
    )

    # Consulta somente a comissão técnica do Santos.
    response = client.get(f"/clubs/{santos_id}/staff")

    # Confirma que a consulta foi bem-sucedida.
    assert response.status_code == 200

    # Confirma que somente a profissional do Santos foi retornada.
    staff_members = response.json()
    assert len(staff_members) == 1
    assert staff_members[0]["name"] == "Ana Silva"
    assert staff_members[0]["club_id"] == santos_id
