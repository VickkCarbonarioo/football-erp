
# Importa BaseModel e Field para estruturar e validar os dados.
from pydantic import BaseModel, Field

# Importa o validador de campos do Pydantic.
from pydantic import field_validator


# Define os dados recebidos ao cadastrar um clube.
class ClubCreate(BaseModel):
    # O nome deve ter, no mínimo, um caractere.
    name: str = Field(min_length=1)

    # Valida o nome antes das demais validações.
    @field_validator("name", mode="before")
    @classmethod
    def validate_name(cls, value):
        # Remove espaços das extremidades quando o valor é texto.
        if isinstance(value, str):
            value = value.strip()

        # Retorna o valor para continuar a validação.
        return value


# Define os dados recebidos ao cadastrar um profissional.
class StaffMemberCreate(BaseModel):
    # Nome do profissional, limitado a 100 caracteres.
    name: str = Field(min_length=1, max_length=100)

    # Cargo do profissional, limitado a 100 caracteres.
    role: str = Field(min_length=1, max_length=100)

    # Identificador do clube ao qual pertence.
    club_id: int = Field(gt=0)

    # Valida o nome antes das demais validações.
    @field_validator("name", mode="before")
    @classmethod
    def validate_name(cls, value):
        # Remove espaços das extremidades quando o valor é texto.
        if isinstance(value, str):
            value = value.strip()

        # Retorna o valor para continuar a validação.
        return value

    # Valida o cargo antes das demais validações.
    @field_validator("role", mode="before")
    @classmethod
    def validate_role(cls, value):
        # Remove espaços das extremidades quando o valor é texto.
        if isinstance(value, str):
            value = value.strip()

        # Retorna o valor para continuar a validação.
        return value

    