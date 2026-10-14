
# Importa a classe BaseModel, utilizada para validar dados.
from pydantic import BaseModel

# Define o formato dos dados recebidos ao cadastrar um clube.
class ClubCreate(BaseModel):
    # O nome do clube deve ser um texto.
    name: str
