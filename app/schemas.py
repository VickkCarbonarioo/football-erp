# Importa BaseModel e Field, utilizados para estruturar e validar dados.
from pydantic import BaseModel, Field

# Importa o validador de campos do Pydantic.
from pydantic import field_validator


# Define o formato dos dados recebidos ao cadastrar um clube.
class ClubCreate(BaseModel):
    # O nome deve ser um texto com, no mínimo, um caractere.
    name: str = Field(min_length=1)

    # Executa a validação antes de aceitar o nome.
    @field_validator("name", mode="before")
    @classmethod
    def validate_name(cls, value):
        # Se o valor recebido for um texto, remove espaços das extremidades.
        if isinstance(value, str):
            value = value.strip()

        # Retorna o valor para que o Pydantic continue a validação.
        return value
    