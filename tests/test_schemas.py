
# Importa o schema responsável pela validação dos clubes.
from app.schemas import ClubCreate

# Importa a exceção gerada quando os dados são inválidos.
from pydantic import ValidationError

# Importa o pytest para verificar erros esperados.
import pytest


# Verifica se um nome válido é aceito.
def test_club_name_valid():
    club = ClubCreate(name="Corinthians")

    assert club.name == "Corinthians"


# Verifica se espaços nas extremidades são removidos.
def test_club_name_strips_whitespace():
    club = ClubCreate(name="  Corinthians  ")

    assert club.name == "Corinthians"


# Verifica se um nome vazio é rejeitado.
def test_club_name_rejects_empty_string():
    with pytest.raises(ValidationError):
        ClubCreate(name="")


# Verifica se um nome composto apenas por espaços é rejeitado.
def test_club_name_rejects_whitespace_only():
    with pytest.raises(ValidationError):
        ClubCreate(name="   ")
