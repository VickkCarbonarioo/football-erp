
# Importa as funções do serviço de equipes que serão testadas.
from app.team_service import create_team, list_teams_by_club

# Importa a função que cadastra clubes para preparar os testes.
from app.club_service import create_club


# Verifica se uma equipe é cadastrada corretamente.
def test_create_team_returns_created_team(client):
    # Cria um clube para vincular à equipe.
    club = create_club("Santos")

    # Cadastra uma equipe vinculada ao clube criado.
    team = create_team(
        name="Sub-17",
        category="Base",
        gender="Masculino",
        age_group="Sub-17",
        club_id=club.id,
    )

    # Confirma que a equipe foi criada.
    assert team is not None

    # Confirma que o nome foi salvo corretamente.
    assert team.name == "Sub-17"

    # Confirma que a equipe está vinculada ao clube correto.
    assert team.club_id == club.id

    # Confirma que o status padrão foi aplicado.
    assert team.status == "active"

    # Confirma que as datas foram preenchidas.
    assert team.created_at is not None
    assert team.updated_at is not None


# Verifica se o serviço rejeita um clube inexistente.
def test_create_team_returns_none_when_club_not_found(client):
    # Tenta cadastrar uma equipe vinculada a um clube inexistente.
    team = create_team(
        name="Sub-20",
        category="Base",
        gender="Masculino",
        age_group="Sub-20",
        club_id=99999,
    )

    # Confirma que a equipe não foi cadastrada.
    assert team is None


# Verifica se a listagem retorna somente equipes do clube informado.
def test_list_teams_by_club_returns_only_matching_teams(client):
    # Cria dois clubes diferentes.
    santos = create_club("Santos")
    palmeiras = create_club("Palmeiras")

    # Cadastra uma equipe para cada clube.
    create_team(
        name="Sub-17 Santos",
        category="Base",
        gender="Masculino",
        age_group="Sub-17",
        club_id=santos.id,
    )

    create_team(
        name="Sub-20 Palmeiras",
        category="Base",
        gender="Masculino",
        age_group="Sub-20",
        club_id=palmeiras.id,
    )

    # Lista as equipes do Santos.
    teams = list_teams_by_club(santos.id)

    # Confirma que apenas uma equipe foi encontrada.
    assert len(teams) == 1

    # Confirma que a equipe encontrada pertence ao Santos.
    assert teams[0].name == "Sub-17 Santos"
    assert teams[0].club_id == santos.id


# Verifica se a listagem retorna uma lista vazia sem equipes.
def test_list_teams_by_club_returns_empty_list(client):
    # Cria um clube sem cadastrar equipes.
    club = create_club("Corinthians")

    # Busca as equipes do clube.
    teams = list_teams_by_club(club.id)

    # Confirma que a lista está vazia.
    assert teams == []
