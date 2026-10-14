
# Importa Session para realizar operações no banco de dados.
from sqlalchemy.orm import Session

# Importa o mecanismo de conexão com o banco.
from app.database import engine

# Importa o modelo que representa os clubes.
from app.models import Club


# Define uma função que recebe o nome de um clube.

# Define uma função que recebe o nome de um clube.
def create_club(name: str):

    # Abre uma sessão para trabalhar com o banco.
    with Session(engine) as session:

        # Procura um clube com o mesmo nome.
        existing_club = session.query(Club).filter(
            Club.name == name
        ).first()

        # Impede o cadastro de um nome já existente.
        if existing_club:
            return None

        # Cria um objeto que representa o novo clube.
        club = Club(name=name)

        # Adiciona o clube à sessão.
        session.add(club)

        # Salva a alteração definitivamente no banco.
        session.commit()

        # Atualiza os dados do objeto após o cadastro.
        session.refresh(club)

        # Retorna o clube criado para quem chamou a função.
        return club



# Define uma função para listar todos os clubes cadastrados.
def list_clubs():

    # Abre uma sessão para consultar o banco de dados.
    with Session(engine) as session:

        # Busca todos os registros da tabela Club.
        clubs = session.query(Club).all()

        # Retorna os clubes encontrados para quem chamou a função.
        return clubs

    
# Define uma função para buscar um clube pelo seu ID.
def get_club_by_id(club_id: int):

    # Abre uma sessão para consultar o banco de dados.
    with Session(engine) as session:

        # Procura o clube que possui o ID informado.
        club = session.query(Club).filter(
            Club.id == club_id
        ).first()

        # Retorna o clube encontrado ou None se não existir.
        return club

