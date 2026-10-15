# Importa as funções do serviço de jogadores que serão testadas.
from app.player_service import create_player, list_players_by_team

# Importa as funções usadas para preparar os dados dos testes.
from app.club_service import create_club
from app.team_service import create_team

# Importa date para criar uma data de nascimento nos testes.
from datetime import date


# Verifica se um jogador é cadastrado corretamente.
def test_create_player_returns_created_player(client):
    # Cria um clube para servir de base à equipe.
    club = create_club("Santos")

    # Cria uma equipe vinculada ao clube.
    team = create_team(
        name="Sub-17",
        category="Base",
        gender="Masculino",
        age_group="Sub-17",
        club_id=club.id,
    )

    # Cadastra um jogador vinculado à equipe criada.
    player = create_player(
        name="João Silva",
        birth_date=date(2005, 4, 15),
        nationality="Brazilian",
        dominant_foot="right",
        height_cm=180,
        shirt_number=9,
        team_id=team.id,
    )

    # Confirma que o jogador foi cadastrado.
    assert player is not None

    # Confirma que os dados principais foram salvos corretamente.
    assert player.name == "João Silva"
    assert player.birth_date == date(2005, 4, 15)
    assert player.nationality == "Brazilian"
    assert player.dominant_foot == "right"
    assert player.height_cm == 180
    assert player.shirt_number == 9

    # Confirma que o jogador está vinculado à equipe correta.
    assert player.team_id == team.id

    # Confirma que o status padrão foi aplicado.
    assert player.status == "active"

    # Confirma que as datas de criação e atualização foram preenchidas.
    assert player.created_at is not None
    assert player.updated_at is not None
    # Verifica se o serviço rejeita uma equipe inexistente.
def test_create_player_returns_none_when_team_not_found(client):
    # Tenta cadastrar um jogador vinculado a uma equipe inexistente.
    player = create_player(
        name="João Silva",
        birth_date=date(2005, 4, 15),
        nationality="Brazilian",
        dominant_foot="right",
        height_cm=180,
        shirt_number=9,
        team_id=99999,
    )

    # Confirma que o jogador não foi cadastrado.
    assert player is None
    # Verifica se a listagem retorna somente jogadores da equipe informada.
def test_list_players_by_team_returns_only_matching_players(client):
    # Cria um clube para vincular as equipes.
    club = create_club("Santos")

    # Cria duas equipes diferentes dentro do mesmo clube.
    team_sub17 = create_team(
        name="Sub-17",
        category="Base",
        gender="Masculino",
        age_group="Sub-17",
        club_id=club.id,
    )

    team_sub20 = create_team(
        name="Sub-20",
        category="Base",
        gender="Masculino",
        age_group="Sub-20",
        club_id=club.id,
    )

    # Cadastra um jogador na equipe Sub-17.
    create_player(
        name="João Silva",
        birth_date=date(2005, 4, 15),
        nationality="Brazilian",
        dominant_foot="right",
        height_cm=180,
        shirt_number=9,
        team_id=team_sub17.id,
    )

    # Cadastra outro jogador na equipe Sub-20.
    create_player(
        name="Pedro Santos",
        birth_date=date(2004, 8, 20),
        nationality="Brazilian",
        dominant_foot="left",
        height_cm=175,
        shirt_number=10,
        team_id=team_sub20.id,
    )

    # Busca os jogadores da equipe Sub-17.
    players = list_players_by_team(team_sub17.id)

    # Confirma que somente um jogador foi encontrado.
    assert len(players) == 1

    # Confirma que o jogador pertence à equipe solicitada.
    assert players[0].name == "João Silva"
    assert players[0].team_id == team_sub17.id
    # Verifica se a listagem retorna uma lista vazia quando não há jogadores.
def test_list_players_by_team_returns_empty_list(client):
    # Cria um clube para servir de base à equipe.
    club = create_club("Corinthians")

    # Cria uma equipe sem cadastrar nenhum jogador.
    team = create_team(
        name="Sub-17",
        category="Base",
        gender="Masculino",
        age_group="Sub-17",
        club_id=club.id,
    )

    # Busca os jogadores da equipe recém-criada.
    players = list_players_by_team(team.id)

    # Confirma que nenhum jogador foi encontrado.
    assert players == []