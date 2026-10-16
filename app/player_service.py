
# Importa Session para realizar operações no banco de dados.
from sqlalchemy.orm import Session

# Importa o mecanismo de conexão com o banco.
from app.database import engine

# Importa os modelos de equipe e jogador.
from app.models import Team, Player

# Importa date para indicar o tipo da data de nascimento.
from datetime import date


# Define uma função para cadastrar um jogador.
def create_player(
    name: str,
    birth_date: date,
    nationality: str,
    dominant_foot: str | None,
    height_cm: int,
    shirt_number: int,
    team_id: int,
    status: str = "active",
):
    # Abre uma sessão para trabalhar com o banco.
    with Session(engine) as session:

        # Verifica se a equipe informada existe.
        team = session.query(Team).filter(
            Team.id == team_id
        ).first()

        # Impede o cadastro se a equipe não existir.
        if not team:
            return None

        # Cria o objeto que representa o novo jogador.
        player = Player(
            name=name,
            birth_date=birth_date,
            nationality=nationality,
            dominant_foot=dominant_foot,
            height_cm=height_cm,
            shirt_number=shirt_number,
            team_id=team_id,
            status=status,
        )

        # Adiciona o jogador à sessão.
        session.add(player)

        # Salva o cadastro no banco.
        session.commit()

        # Atualiza o objeto com os dados gerados pelo banco.
        session.refresh(player)

        # Retorna o jogador cadastrado.
        return player


# Define uma função para listar os jogadores de uma equipe.
def list_players_by_team(team_id: int):

    # Abre uma sessão para consultar o banco.
    with Session(engine) as session:

        # Busca somente os jogadores da equipe informada.
        players = session.query(Player).filter(
            Player.team_id == team_id
        ).all()

        # Retorna a lista de jogadores encontrados.
        return players


# Define uma função para buscar um jogador pelo ID.
def get_player_by_id(player_id: int):

    # Abre uma sessão para consultar o banco de dados.
    with Session(engine) as session:

        # Busca o jogador que corresponde ao ID informado.
        player = session.query(Player).filter(
            Player.id == player_id
        ).first()

        # Retorna o jogador encontrado ou None se não existir.
        return player
