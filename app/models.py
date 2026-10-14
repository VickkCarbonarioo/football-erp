
# Importa os recursos necessários para definir colunas e tipos de dados.
from sqlalchemy import String
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
