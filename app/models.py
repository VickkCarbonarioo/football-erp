# Importa date para datas sem horário e datetime/timezone para registros de data e hora.
from datetime import date, datetime, timezone
# Importa os tipos de dados usados nas tabelas do sistema.
from sqlalchemy import (
    String,
    ForeignKey,
    DateTime,
    Date,
    Integer,
    Numeric,
)
# Importa recursos para tipar e mapear as colunas dos modelos.
from sqlalchemy.orm import Mapped, mapped_column
# Importa a Base usada para registrar os modelos do banco.
from app.database import Base
from decimal import Decimal

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
    # Define o modelo que representará os jogadores no banco de dados.
class Player(Base):
    # Define o nome da tabela que será criada no banco.
    __tablename__ = "players"

    # Identificador único de cada jogador.
    id: Mapped[int] = mapped_column(primary_key=True)

    # ID da equipe à qual o jogador pertence.
    # A chave estrangeira exige uma equipe existente.
    team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id"),
        nullable=False,
    )

    # Nome completo do jogador.
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    # Data de nascimento, armazenada sem horário.
    birth_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    # Nacionalidade do jogador.
    nationality: Mapped[str] = mapped_column(
        String(60),
        nullable=False,
    )

    # Pé dominante do jogador.
    # Permanece opcional enquanto não definirmos regras específicas.
    dominant_foot: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True,
    )

    # Altura do jogador em centímetros.
    height_cm: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    # Número da camisa do jogador.
    shirt_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    # Situação atual do jogador, com padrão active.
    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="active",
    )

    # Data e hora em que o registro foi criado.
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    # Data e hora da última atualização do registro.
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    # Importa Decimal para representar valores monetários com precisão.
from decimal import Decimal


# Define o modelo que representará os contratos dos jogadores.
class Contract(Base):

    # Define o nome da tabela no banco de dados.
    __tablename__ = "contracts"

    # Identificador único de cada contrato.
    id: Mapped[int] = mapped_column(primary_key=True)

    # ID do jogador vinculado ao contrato.
    # A chave estrangeira exige que o jogador exista.
    player_id: Mapped[int] = mapped_column(
        ForeignKey("players.id"),
        nullable=False,
        index=True,
    )

    # Data em que o contrato começa a valer.
    start_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    # Data prevista para o término do contrato.
    end_date: Mapped[date] = mapped_column(
        Date,
        nullable=False,
    )

    # Salário mensal do jogador, com duas casas decimais.
    monthly_salary: Mapped[Decimal] = mapped_column(
        Numeric(12, 2),
        nullable=False,
    )

    # Valor total do contrato, quando informado.
    # O campo é opcional porque nem todo contrato terá esse valor definido.
    total_value: Mapped[Decimal | None] = mapped_column(
        Numeric(14, 2),
        nullable=True,
    )

    # Data de encerramento antecipado, quando aplicável.
    # None significa que não foi registrado encerramento antecipado.
    terminated_at: Mapped[date | None] = mapped_column(
        Date,
        nullable=True,
    )

    # Data e hora em que o contrato foi criado no sistema.
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
    )

    # Data e hora da última atualização do contrato.
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )