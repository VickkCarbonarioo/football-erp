
# Importa recursos para trabalhar com datas e horários.
from datetime import datetime, timezone

# Importa tipos de dados e chaves estrangeiras do SQLAlchemy.
from sqlalchemy import String, ForeignKey, DateTime

# Importa recursos para tipar e mapear as colunas dos modelos.
from sqlalchemy.orm import Mapped, mapped_column

# Importa a Base usada para registrar os modelos do banco.
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
# Define o modelo que representará as equipes no banco de dados.
class Team(Base):
    # Define o nome da tabela que será associada a este modelo.
    __tablename__ = "teams"

    # Identificador único de cada equipe.
    id: Mapped[int] = mapped_column(primary_key=True)

    # ID do clube ao qual a equipe pertence.
    # A chave estrangeira aponta para a tabela clubs.
    club_id: Mapped[int] = mapped_column(
        ForeignKey("clubs.id"),
        nullable=False,
    )

    # Nome da equipe.
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    # Categoria da equipe.
    category: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    # Gênero ou classificação da equipe.
    gender: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    # Faixa etária, como Sub-17 ou Sub-20.
    age_group: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
    )

    # Situação atual da equipe.
    # Se nenhum valor for informado, começa como active.
    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="active",
    )

    # Data e hora em que a equipe foi criada.
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    # Data e hora da última atualização da equipe.
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )