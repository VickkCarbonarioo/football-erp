
# Importa recursos para criar e gerenciar testes.
import pytest

# Importa o mecanismo de conexão com o banco de dados.
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

# Importa o cliente de testes do FastAPI.
from fastapi.testclient import TestClient

# Importa a aplicação principal.
from app.main import app

# Importa a base declarativa dos modelos.
from app.database import Base
# Importa os modelos para registrá-los na Base antes de criar as tabelas.
from app.models import Club, StaffMember, Team

# Importa os serviços para direcioná-los ao banco de teste.
import app.club_service as club_service
import app.staff_service as staff_service
import app.team_service as team_service

# Executa esta configuração antes de cada teste.
@pytest.fixture
def client():
    # Cria um banco SQLite temporário em memória.
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # Cria as tabelas dos modelos no banco de teste.
    Base.metadata.create_all(bind=test_engine)

    # Guarda os engines originais dos dois serviços.
    original_club_engine = club_service.engine
    original_staff_engine = staff_service.engine
    original_team_engine = team_service.engine

    # Direciona os dois serviços para o banco de teste.
    club_service.engine = test_engine
    staff_service.engine = test_engine
    team_service.engine = test_engine

    try:
        # Cria o cliente que permite chamar a API nos testes.
        with TestClient(app) as test_client:
            yield test_client

    finally:
        # Restaura os engines originais dos serviços.
        club_service.engine = original_club_engine
        staff_service.engine = original_staff_engine
        team_service.engine = original_team_engine

        # Remove as tabelas do banco temporário.
        Base.metadata.drop_all(bind=test_engine)

        # Encerra as conexões do banco de teste.
        test_engine.dispose()


