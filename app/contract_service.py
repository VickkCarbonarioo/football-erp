
# Importa Decimal para representar valores monetários com precisão.
from decimal import Decimal

# Importa date para trabalhar com as datas dos contratos.
from datetime import date

# Importa Session para realizar operações no banco de dados.
from sqlalchemy.orm import Session

# Importa o mecanismo de conexão com o banco.
from app.database import engine

# Importa os modelos de jogador e contrato.
from app.models import Player, Contract


# Define uma função para cadastrar um contrato.
def create_contract(
    player_id: int,
    start_date: date,
    end_date: date,
    monthly_salary: Decimal,
    total_value: Decimal | None = None,
):
    # Abre uma sessão para trabalhar com o banco.
    with Session(engine) as session:

        # Verifica se o jogador informado existe.
        player = session.query(Player).filter(
            Player.id == player_id
        ).first()

        # Impede o cadastro se o jogador não existir.
        if not player:
            return None

        # Cria o objeto que representa o novo contrato.
        contract = Contract(
            player_id=player_id,
            start_date=start_date,
            end_date=end_date,
            monthly_salary=monthly_salary,
            total_value=total_value,
        )

        # Adiciona o contrato à sessão.
        session.add(contract)

        # Salva o contrato no banco de dados.
        session.commit()

        # Atualiza o objeto com os dados gerados pelo banco.
        session.refresh(contract)

        # Retorna o contrato cadastrado.
        return contract


# Define uma função para listar os contratos de um jogador.
def list_contracts_by_player(player_id: int):
    # Abre uma sessão para consultar o banco.
    with Session(engine) as session:

        # Verifica se o jogador existe.
        player = session.query(Player).filter(
            Player.id == player_id
        ).first()

        # Retorna None quando o jogador não existe.
        if not player:
            return None

        # Busca os contratos do jogador,
        # ordenando do mais recente para o mais antigo.
        contracts = session.query(Contract).filter(
            Contract.player_id == player_id
        ).order_by(Contract.start_date.desc()).all()

        # Retorna a lista de contratos encontrados.
        # Se não houver contratos, retorna uma lista vazia.
        return contracts


# Define uma função para encerrar um contrato antecipadamente.
def terminate_contract(
    contract_id: int,
    terminated_at: date,
):
    # Abre uma sessão para trabalhar com o banco.
    with Session(engine) as session:

        # Busca o contrato pelo ID informado.
        contract = session.query(Contract).filter(
            Contract.id == contract_id
        ).first()

        # Retorna None se o contrato não existir.
        if not contract:
            return None

        # Impede que um contrato seja encerrado novamente.
        if contract.terminated_at is not None:
            return False

        # Impede o encerramento antes do início do contrato.
        if terminated_at < contract.start_date:
            return False

        # Impede o encerramento depois do fim previsto.
        if terminated_at > contract.end_date:
            return False

        # Registra a data do encerramento antecipado.
        contract.terminated_at = terminated_at

        # Salva a alteração no banco de dados.
        session.commit()

        # Atualiza o objeto com os dados salvos.
        session.refresh(contract)

        # Retorna o contrato atualizado.
        return contract
