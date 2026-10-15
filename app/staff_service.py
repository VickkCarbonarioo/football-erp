
# Importa Session para realizar operações no banco de dados.
from sqlalchemy.orm import Session

# Importa o mecanismo de conexão com o banco.
from app.database import engine

# Importa os modelos de clube e de profissional da comissão técnica.
from app.models import Club, StaffMember


# Define uma função para cadastrar um profissional da comissão técnica.
def create_staff_member(name: str, role: str, club_id: int):

    # Abre uma sessão para trabalhar com o banco.
    with Session(engine) as session:

        # Procura o clube ao qual o profissional será vinculado.
        club = session.query(Club).filter(
            Club.id == club_id
        ).first()

        # Impede o cadastro se o clube não existir.
        if not club:
            return None

        # Cria um objeto com os dados do profissional.
        staff_member = StaffMember(
            name=name,
            role=role,
            club_id=club_id,
        )

        # Adiciona o profissional à sessão.
        session.add(staff_member)

        # Salva o cadastro no banco de dados.
        session.commit()

        # Atualiza o objeto com os dados gerados pelo banco.
        session.refresh(staff_member)

        # Retorna o profissional cadastrado.
        return staff_member


# Define uma função para listar a comissão técnica de um clube.
def list_staff_members_by_club(club_id: int):

    # Abre uma sessão para consultar o banco de dados.
    with Session(engine) as session:

        # Busca todos os profissionais vinculados ao clube informado.
        staff_members = session.query(StaffMember).filter(
            StaffMember.club_id == club_id
        ).all()

        # Retorna a lista de profissionais encontrados.
        return staff_members
