
# Importa a função que queremos testar.
from app.club_service import create_club, list_clubs, get_club_by_id


# Verifica se a função cria um clube corretamente.
def test_create_club_returns_created_club(client):
    # Cria um clube usando o serviço.
    club = create_club("Santos")

    # Confirma que um clube foi retornado.
    assert club is not None

    # Confirma que o nome foi salvo corretamente.
    assert club.name == "Santos"

    # Confirma que o banco atribuiu um ID ao clube.
    assert club.id is not None


# Verifica se o serviço impede o cadastro de clubes duplicados.
def test_create_duplicate_club_returns_none(client):
    # Cria o clube pela primeira vez.
    first_club = create_club("Corinthians")

    # Tenta cadastrar novamente o mesmo clube.
    duplicate_club = create_club("Corinthians")

    # Confirma que o primeiro cadastro funcionou.
    assert first_club is not None

    # Confirma que o segundo cadastro foi rejeitado.
    assert duplicate_club is None


# Verifica se o serviço retorna uma lista vazia quando não há clubes.
def test_list_clubs_returns_empty_list(client):
    # Busca os clubes cadastrados no banco de teste.
    clubs = list_clubs()

    # Confirma que o resultado é uma lista vazia.
    assert clubs == []

# Verifica se o serviço lista os clubes cadastrados.
def test_list_clubs_returns_registered_clubs(client):
    # Cadastra dois clubes no banco de teste.
    create_club("Santos")
    create_club("Palmeiras")

    # Busca todos os clubes cadastrados.
    clubs = list_clubs()

    # Confirma que os dois clubes foram encontrados.
    assert len(clubs) == 2

    # Extrai os nomes dos clubes encontrados.
    club_names = [club.name for club in clubs]

    # Confirma que os nomes estão na lista.
    assert "Santos" in club_names
    assert "Palmeiras" in club_names


# Verifica se o serviço encontra um clube pelo ID.
def test_get_club_by_id_returns_club(client):
    # Cadastra um clube no banco de teste.
    created_club = create_club("Corinthians")

    # Busca o clube usando o ID gerado no cadastro.
    found_club = get_club_by_id(created_club.id)

    # Confirma que o clube foi encontrado.
    assert found_club is not None

    # Confirma que o ID corresponde ao clube cadastrado.
    assert found_club.id == created_club.id

    # Confirma que o nome corresponde ao clube cadastrado.
    assert found_club.name == "Corinthians"

# Verifica se o serviço retorna None para um ID inexistente.
def test_get_club_by_id_returns_none_when_not_found(client):
    # Busca um clube usando um ID que não existe.
    club = get_club_by_id(99999)

    # Confirma que nenhum clube foi encontrado.
    assert club is None
