
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


# Define os dados recebidos ao cadastrar uma equipe.
class TeamCreate(BaseModel):
    # Nome da equipe, limitado a 100 caracteres.
    name: str = Field(min_length=1, max_length=100)

    # Categoria da equipe, limitada a 50 caracteres.
    category: str = Field(min_length=1, max_length=50)

    # Gênero ou classificação, limitado a 30 caracteres.
    gender: str = Field(min_length=1, max_length=30)

    # Faixa etária, limitada a 30 caracteres.
    age_group: str = Field(min_length=1, max_length=30)

    # ID do clube ao qual a equipe pertence.
    club_id: int = Field(gt=0)

    # Situação da equipe, com valor padrão active.
    status: str = Field(default="active", min_length=1, max_length=30)

    # Remove espaços das extremidades dos campos de texto.
    @field_validator(
        "name",
        "category",
        "gender",
        "age_group",
        "status",
        mode="before",
    )
    @classmethod
    def validate_text_fields(cls, value):
        # Remove espaços extras quando o valor recebido é texto.
        if isinstance(value, str):
            value = value.strip()

        # Devolve o valor para as validações do Pydantic.
        return value

    