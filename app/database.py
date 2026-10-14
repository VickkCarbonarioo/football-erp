
# Importa a função create_engine, responsável por criar a conexão
# entre nossa aplicação e o banco de dados.
from sqlalchemy import create_engine


# Define o endereço do banco de dados SQLite.
# O arquivo football_erp.db será criado quando a conexão for utilizada.
DATABASE_URL = "sqlite:///./football_erp.db"


# Cria o mecanismo de conexão com o banco de dados.
# O SQLAlchemy utilizará esse mecanismo para se comunicar com o SQLite.
engine = create_engine(
    DATABASE_URL,
    echo=True,
)

# Importa o recurso que cria a base das nossas classes de modelo.
from sqlalchemy.orm import DeclarativeBase


# Define a classe-base que nossos modelos de banco de dados utilizarão.
class Base(DeclarativeBase):
    # Por enquanto, não precisamos adicionar comportamento próprio.
    pass
