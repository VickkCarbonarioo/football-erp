
def test_list_clubs_returns_empty_list(client):
    # Faz uma requisição para listar os clubes.
    response = client.get("/clubs")

    # Verifica se a API respondeu com sucesso.
    assert response.status_code == 200

    # Verifica se o banco de testes começa sem clubes.
    assert response.json() == []

def test_create_club_returns_created_club(client):
    # Envia os dados do clube para a API.
    response = client.post(
        "/clubs",
        json={"name": "Corinthians"},
    )

    # Verifica se o clube foi criado.
    assert response.status_code == 201

    # Verifica se o nome retornado está correto.
    assert response.json()["name"] == "Corinthians"

    # Verifica se o clube recebeu um ID.
    assert response.json()["id"] is not None


def test_create_duplicate_club_returns_conflict(client):
    # Cadastra o primeiro clube.
    client.post(
        "/clubs",
        json={"name": "Corinthians"},
    )

    # Tenta cadastrar o mesmo clube novamente.
    response = client.post(
        "/clubs",
        json={"name": "Corinthians"},
    )

    # Confirma que a API rejeita a duplicidade.
    assert response.status_code == 409

    # Confirma a mensagem de erro esperada.
    assert response.json()["detail"] == "Este clube já está cadastrado."


def test_get_club_by_id_returns_club(client):
    # Cadastra um clube para realizar a consulta.
    create_response = client.post(
        "/clubs",
        json={"name": "Palmeiras"},
    )

    # Obtém o ID gerado pela API.
    club_id = create_response.json()["id"]

    # Consulta o clube pelo ID.
    response = client.get(f"/clubs/{club_id}")

    # Verifica se a consulta foi bem-sucedida.
    assert response.status_code == 200

    # Confirma que os dados retornados são do clube correto.
    assert response.json()["id"] == club_id
    assert response.json()["name"] == "Palmeiras"


def test_get_nonexistent_club_returns_not_found(client):
    # Consulta um ID que não existe no banco de testes.
    response = client.get("/clubs/99999")

    # Verifica se a API informa que o clube não foi encontrado.
    assert response.status_code == 404

    # Confirma a mensagem de erro retornada.
    assert response.json()["detail"] == "Clube não encontrado."
