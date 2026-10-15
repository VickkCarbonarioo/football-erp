
# Importa os schemas usados para validar clubes e jogadores.
from app.schemas import ClubCreate, PlayerCreate
# Importa a exceção gerada quando os dados são inválidos.
from pydantic import ValidationError
# Importa o pytest para verificar erros esperados.
import pytest
# Verifica se um nome válido é aceito.
def test_club_name_valid():
    club = ClubCreate(name="Corinthians")

    assert club.name == "Corinthians"


# Verifica se espaços nas extremidades são removidos.
def test_club_name_strips_whitespace():
    club = ClubCreate(name="  Corinthians  ")

    assert club.name == "Corinthians"


# Verifica se um nome vazio é rejeitado.
def test_club_name_rejects_empty_string():
    with pytest.raises(ValidationError):
        ClubCreate(name="")


# Verifica se um nome composto apenas por espaços é rejeitado.
def test_club_name_rejects_whitespace_only():
    with pytest.raises(ValidationError):
        ClubCreate(name="   ")


# Importa o schema responsável pela validação das equipes.
from app.schemas import TeamCreate


# Verifica se uma equipe válida é aceita.
def test_team_schema_accepts_valid_data():
    # Cria uma equipe com dados válidos.
    team = TeamCreate(
        name="Sub-17",
        category="Base",
        gender="Masculino",
        age_group="Sub-17",
        club_id=1,
    )

    # Confirma que os dados foram aceitos.
    assert team.name == "Sub-17"
    assert team.club_id == 1

    # Confirma que o status padrão foi aplicado.
    assert team.status == "active"


# Verifica se espaços nas extremidades são removidos.
def test_team_schema_strips_whitespace():
    # Cria uma equipe com espaços extras nos textos.
    team = TeamCreate(
        name="  Sub-17  ",
        category="  Base  ",
        gender=" Masculino ",
        age_group=" Sub-17 ",
        club_id=1,
    )

    # Confirma que os espaços foram removidos.
    assert team.name == "Sub-17"
    assert team.category == "Base"
    assert team.gender == "Masculino"
    assert team.age_group == "Sub-17"


# Verifica se um nome vazio é rejeitado.
def test_team_schema_rejects_empty_name():
    with pytest.raises(ValidationError):
        TeamCreate(
            name="",
            category="Base",
            gender="Masculino",
            age_group="Sub-17",
            club_id=1,
        )


# Verifica se um ID de clube inválido é rejeitado.
def test_team_schema_rejects_invalid_club_id():
    with pytest.raises(ValidationError):
        TeamCreate(
            name="Sub-17",
            category="Base",
            gender="Masculino",
            age_group="Sub-17",
            club_id=0,
        )
        # Verifica se os dados válidos de um jogador são aceitos.
def test_player_schema_accepts_valid_data():
    # Cria um jogador com todos os campos obrigatórios preenchidos.
    player = PlayerCreate(
        name="  João Silva  ",
        birth_date="2005-04-15",
        nationality="  Brazilian  ",
        dominant_foot="right",
        height_cm=180,
        shirt_number=9,
        team_id=1,
    )

    # Confirma que os espaços extras foram removidos.
    assert player.name == "João Silva"
    assert player.nationality == "Brazilian"

    # Confirma que a data foi convertida para o tipo date.
    assert player.birth_date.isoformat() == "2005-04-15"

    # Confirma os demais campos.
    assert player.dominant_foot == "right"
    assert player.height_cm == 180
    assert player.shirt_number == 9
    assert player.team_id == 1

    # Confirma que o status padrão foi aplicado.
    assert player.status == "active"
    # Verifica se os três valores permitidos para o pé dominante são aceitos.
@pytest.mark.parametrize("dominant_foot", ["right", "left", "both"])
def test_player_schema_accepts_valid_dominant_foot(dominant_foot):
    # Cria um jogador usando o valor de pé dominante recebido no teste.
    player = PlayerCreate(
        name="João Silva",
        birth_date="2005-04-15",
        nationality="Brazilian",
        dominant_foot=dominant_foot,
        height_cm=180,
        shirt_number=9,
        team_id=1,
    )

    # Confirma que o valor foi aceito e preservado.
    assert player.dominant_foot == dominant_foot


# Verifica se um valor não permitido para o pé dominante é rejeitado.
def test_player_schema_rejects_invalid_dominant_foot():
    # Espera um erro de validação ao informar um valor inválido.
    with pytest.raises(ValidationError):
        PlayerCreate(
            name="João Silva",
            birth_date="2005-04-15",
            nationality="Brazilian",
            dominant_foot="middle",
            height_cm=180,
            shirt_number=9,
            team_id=1,
        )
