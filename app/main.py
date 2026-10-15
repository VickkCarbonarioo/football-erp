
from fastapi import FastAPI, HTTPException

# Importa os serviços de clubes.
from app.club_service import list_clubs, create_club, get_club_by_id

# Importa os serviços da comissão técnica.
from app.staff_service import create_staff_member, list_staff_members_by_club

# Importa os serviços de equipes.
from app.team_service import create_team, list_teams_by_club

# Importa os schemas de validação da API.
from app.schemas import ClubCreate, StaffMemberCreate, TeamCreate


# Cria a aplicação principal do Football ERP.
# A partir deste objeto vamos registrar nossas rotas,
# configurações e funcionalidades da API.
app = FastAPI(
    title="Football ERP",
    description="Sistema ERP para gestão estratégica de clubes de futebol.",
    version="0.1.0"
)


# Rota inicial da API.
# Quando alguém acessar "/", o sistema executará esta função.
@app.get("/")
def home():
    return {
        "message": "Football ERP está funcionando!",
        "version": "0.1.0"
    }

# Rota para consultar todos os clubes cadastrados.
@app.get("/clubs")
def get_clubs():
    # Busca os clubes utilizando o serviço existente.
    clubs = list_clubs()

    # Converte os dados dos clubes para uma resposta JSON.
    return [
        {
            "id": club.id,
            "name": club.name
        }
        for club in clubs
    ]

# Rota para cadastrar um novo clube.
@app.post("/clubs", status_code=201)
def post_club(club_data: ClubCreate):

    # Envia o nome recebido para o serviço de cadastro.
    club = create_club(club_data.name)

    # Verifica se o serviço identificou um clube duplicado.
    if club is None:
        raise HTTPException(
        status_code=409,
        detail="Este clube já está cadastrado."
    )

    # Retorna os dados do clube cadastrado.
    return {
        "id": club.id,
        "name": club.name
    }


# Rota para consultar um clube específico pelo seu ID.
@app.get("/clubs/{club_id}")
def get_club(club_id: int):

    # Busca o clube utilizando o serviço existente.
    club = get_club_by_id(club_id)

    # Verifica se o clube foi encontrado.
    if club is None:
        raise HTTPException(
            status_code=404,
            detail="Clube não encontrado."
        )

    # Retorna os dados do clube encontrado.
    return {
        "id": club.id,
        "name": club.name
    }


# Rota para cadastrar um profissional da comissão técnica.
@app.post("/staff", status_code=201)
def post_staff_member(staff_data: StaffMemberCreate):

    # Envia os dados recebidos para o serviço de cadastro.
    staff_member = create_staff_member(
        name=staff_data.name,
        role=staff_data.role,
        club_id=staff_data.club_id,
    )

    # Verifica se o clube informado existe.
    if staff_member is None:
        raise HTTPException(
            status_code=404,
            detail="Clube não encontrado.",
        )

    # Retorna os dados do profissional cadastrado.
    return {
        "id": staff_member.id,
        "name": staff_member.name,
        "role": staff_member.role,
        "club_id": staff_member.club_id,
    }


# Rota para consultar a comissão técnica de um clube.
@app.get("/clubs/{club_id}/staff")
def get_club_staff(club_id: int):

    # Busca o clube utilizando o serviço existente.
    club = get_club_by_id(club_id)

    # Verifica se o clube existe.
    if club is None:
        raise HTTPException(
            status_code=404,
            detail="Clube não encontrado.",
        )

    # Busca todos os profissionais vinculados ao clube.
    staff_members = list_staff_members_by_club(club_id)

    # Retorna os profissionais encontrados em formato JSON.
    return [
        {
            "id": staff_member.id,
            "name": staff_member.name,
            "role": staff_member.role,
            "club_id": staff_member.club_id,
        }
        for staff_member in staff_members
    ]


# Rota para cadastrar uma nova equipe.
@app.post("/teams", status_code=201)
def post_team(team_data: TeamCreate):

    # Envia os dados recebidos para o serviço de cadastro.
    team = create_team(
        name=team_data.name,
        category=team_data.category,
        gender=team_data.gender,
        age_group=team_data.age_group,
        club_id=team_data.club_id,
        status=team_data.status,
    )

    # Verifica se o clube informado existe.
    if team is None:
        raise HTTPException(
            status_code=404,
            detail="Clube não encontrado.",
        )

    # Retorna os dados da equipe cadastrada.
    return {
        "id": team.id,
        "name": team.name,
        "category": team.category,
        "gender": team.gender,
        "age_group": team.age_group,
        "club_id": team.club_id,
        "status": team.status,
        "created_at": team.created_at,
        "updated_at": team.updated_at,
    }


# Rota para listar as equipes vinculadas a um clube.
@app.get("/clubs/{club_id}/teams")
def get_club_teams(club_id: int):

    # Verifica se o clube solicitado existe.
    club = get_club_by_id(club_id)

    # Retorna erro se o clube não existir.
    if club is None:
        raise HTTPException(
            status_code=404,
            detail="Clube não encontrado.",
        )

    # Busca as equipes vinculadas ao clube.
    teams = list_teams_by_club(club_id)

    # Retorna as equipes em formato JSON.
    return [
        {
            "id": team.id,
            "name": team.name,
            "category": team.category,
            "gender": team.gender,
            "age_group": team.age_group,
            "club_id": team.club_id,
            "status": team.status,
            "created_at": team.created_at,
            "updated_at": team.updated_at,
        }
        for team in teams
    ]
