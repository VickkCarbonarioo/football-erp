# Importa os recursos necessários para definir colunas,
# tipos de dados e chaves estrangeiras.
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

# Importa a Base que criamos no arquivo database.py.
from app.database import Base


# Define o modelo que representará a tabela de clubes no banco.
class Club(Base):
    # Informa ao SQLAlchemy o nome da tabela que será criada.
    __tablename__ = "clubs"

    # Define a coluna id como chave primária.
    # Cada clube terá seu próprio identificador.
    id: Mapped[int] = mapped_column(primary_key=True)

    # Define a coluna name para armazenar o nome do clube.
    # String(100) permite armazenar textos de até 100 caracteres.
    name: Mapped[str] = mapped_column(String(100), nullable=False)


# Define o modelo que representará os profissionais da comissão técnica.
class StaffMember(Base):
    # Define o nome da tabela no banco de dados.
    __tablename__ = "staff_members"

    # Identificador único de cada profissional.
    id: Mapped[int] = mapped_column(primary_key=True)

    # Nome completo do profissional.
    name: Mapped[str] = mapped_column(String(100), nullable=False)

    # Cargo do profissional na comissão técnica.
    role: Mapped[str] = mapped_column(String(100), nullable=False)

    # ID do clube ao qual o profissional pertence.
    # A chave estrangeira aponta para a tabela clubs.
    club_id: Mapped[int] = mapped_column(
        ForeignKey("clubs.id"),
        nullable=False,
    )
