
# Importa recursos para criar e gerenciar testes.
import pytest

# Importa o mecanismo de conexão e a base dos modelos.
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

# Importa o cliente de testes do FastAPI.
from fastapi.testclient import TestClient

# Importa a aplicação.
from app.main import app

# Importa o modelo para registrar a tabela nos metadados.
from app.models import Club

# Importa a base declarativa.
from app.database import Base

# Importa o módulo de serviços para substituir o engine.
import app.club_service as club_service


# Executa esta configuração antes de cada teste.
@pytest.fixture
def client():
    # Cria um banco SQLite temporário em memória.
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # Cria a tabela de clubes no banco de teste.
    Base.metadata.create_all(bind=test_engine)

    # Guarda o engine original para restaurá-lo depois.
    original_engine = club_service.engine

    # Direciona os serviços para o banco de teste.
    club_service.engine = test_engine

    # Cria o cliente que permite chamar a API nos testes.
    with TestClient(app) as test_client:
        yield test_client

    # Restaura o engine original.
    club_service.engine = original_engine

    # Remove as tabelas do banco de teste.
    Base.metadata.drop_all(bind=test_engine)

    # Encerra as conexões do banco temporário.
    test_engine.dispose()
