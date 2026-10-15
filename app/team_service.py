
# Importa Session para realizar operações no banco de dados.
from sqlalchemy.orm import Session

# Importa o mecanismo de conexão com o banco.
from app.database import engine

# Importa os modelos de clube e equipe.
from app.models import Club, Team


# Define uma função para cadastrar uma equipe.
def create_team(
    name: str,
    category: str,
    gender: str,
    age_group: str,
    club_id: int,
    status: str = "active",
):
    # Abre uma sessão para trabalhar com o banco.
    with Session(engine) as session:

        # Verifica se o clube informado existe.
        club = session.query(Club).filter(
            Club.id == club_id
        ).first()

        # Impede o cadastro se o clube não existir.
        if not club:
            return None

        # Cria o objeto que representa a nova equipe.
        team = Team(
            name=name,
            category=category,
            gender=gender,
            age_group=age_group,
            club_id=club_id,
            status=status,
        )

        # Adiciona a equipe à sessão.
        session.add(team)

        # Salva o cadastro no banco.
        session.commit()

        # Atualiza o objeto com os dados gerados pelo banco.
        session.refresh(team)

        # Retorna a equipe cadastrada.
        return team


# Define uma função para listar as equipes de um clube.
def list_teams_by_club(club_id: int):
    # Abre uma sessão para consultar o banco.
    with Session(engine) as session:

        # Busca as equipes vinculadas ao clube informado.
        teams = session.query(Team).filter(
            Team.club_id == club_id
        ).all()

        # Retorna a lista de equipes encontradas.
        return teams

# Define uma função para buscar uma equipe pelo ID.
def get_team_by_id(team_id: int):
    # Abre uma sessão para consultar o banco de dados.
    with Session(engine) as session:

        # Busca a primeira equipe que corresponde ao ID informado.
        team = session.query(Team).filter(
            Team.id == team_id
        ).first()

        # Retorna a equipe encontrada ou None se ela não existir.
        return team
