# 🗄️ Modelo de Banco de Dados

## 🎯 Objetivo

Este documento descreve as principais entidades do
Football ERP e seus relacionamentos.

O sistema será desenvolvido com uma arquitetura
preparada para múltiplos clubes.

---

## 🧩 Diagrama de entidades

```mermaid
erDiagram

    CLUB ||--o{ TEAM : possui
    TEAM ||--o{ PLAYER : possui
    TEAM ||--o{ STAFF_MEMBER : possui
    TEAM ||--o{ TRAINING_SESSION : realiza
    TEAM ||--o{ MATCH : disputa

    COMPETITION ||--o{ MATCH : possui

    MATCH ||--o{ PLAYER_MATCH : registra
    PLAYER ||--o{ PLAYER_MATCH : participa

    TRAINING_SESSION ||--o{ TRAINING_PARTICIPATION : possui
    PLAYER ||--o{ TRAINING_PARTICIPATION : participa

    USER }o--|| ROLE : possui

## 🔮 Entidades planejadas para versões futuras

As seguintes entidades serão avaliadas e implementadas
conforme a evolução do sistema:

- Periodization
- Macrocycle
- Mesocycle
- Microcycle
- PlayerAvailability
- PlayerInjury
- PlayerLoad
- PhysicalAssessment
- ScoutingReport
- News
- TransferMarket
- TacticalAnalysis

### Player — Campos iniciais

| Campo | Tipo conceitual | Descrição |
|---|---|---|
| id | Identificador | Identificador único do jogador |
| team_id | Relacionamento | Equipe atual do jogador |
| name | Texto | Nome completo |
| birth_date | Data | Data de nascimento |
| nationality | Texto | Nacionalidade |
| dominant_foot | Texto | Pé dominante |
| height_cm | Número | Altura em centímetros |
| shirt_number | Número | Número da camisa |
| status | Texto | Situação atual do cadastro |
| created_at | Data/hora | Data de criação do registro |
| updated_at | Data/hora | Última atualização |

### Relacionamentos planejados

- PlayerPosition
- PlayerRole
- PlayerTeamHistory
- PlayerInjury
- PhysicalAssessment
- PlayerMatch
- TrainingParticipation

---

## 🧬 PhysicalAssessment

Representa uma avaliação física realizada em uma determinada
data.

Os dados devem ser armazenados historicamente, permitindo
comparar a evolução física do atleta ao longo do tempo.

### Exemplos de dados

- Peso
- Massa gorda
- Massa magra
- Percentual de gordura
- Massa muscular
- Percentual de músculo
- IMC
- Medidas antropométricas
- Testes de velocidade
- Testes de resistência
- Testes de força
- Testes de salto
- VO₂máx
- Frequência cardíaca
- Outros testes físicos realizados pelo clube

A estrutura deverá ser extensível para permitir a inclusão
de novos tipos de avaliações sem a necessidade de alterar
constantemente a estrutura principal do jogador.

---

## 🏥 PlayerInjury

Representa uma ocorrência de lesão registrada para um atleta.

Cada lesão deve possuir seu próprio registro histórico.

### Exemplos de informações

- Tipo de lesão
- Região corporal
- Data de início
- Data de retorno
- Gravidade
- Status
- Observações
- Tratamento

## 🏢 Club

Representa um clube de futebol cadastrado no Football ERP.

O sistema foi projetado para suportar múltiplos clubes,
permitindo que a mesma plataforma seja utilizada por
diferentes organizações esportivas.

### Campos iniciais

| Campo | Tipo conceitual | Descrição |
|---|---|---|
| id | Identificador | Identificador único do clube |
| name | Texto | Nome oficial do clube |
| short_name | Texto | Nome curto utilizado pelo sistema |
| nickname | Texto | Apelido do clube |
| country | Texto | País do clube |
| state | Texto | Estado ou região |
| city | Texto | Cidade do clube |
| founded_at | Data | Data de fundação |
| logo_url | Texto | Endereço da imagem do escudo |
| primary_color | Texto | Cor principal do clube |
| secondary_color | Texto | Cor secundária do clube |
| official_website | Texto | Site oficial |
| history | Texto longo | História e informações históricas do clube |
| status | Texto | Situação do clube no sistema |
| created_at | Data/hora | Data de criação do registro |
| updated_at | Data/hora | Última atualização do registro |

### Relacionamentos planejados

- Stadium
- TrainingCenter
- ClubSponsor
- Sponsor
- ClubLeadership
- SocialMediaAccount

## 👥 Team

Representa uma equipe pertencente a um clube.

Um clube pode possuir diversas equipes, como categorias
de base, equipe profissional e equipes femininas.

### Campos iniciais

| Campo | Tipo conceitual | Descrição |
|---|---|---|
| id | Identificador | Identificador único da equipe |
| club_id | Relacionamento | Clube ao qual a equipe pertence |
| name | Texto | Nome da equipe |
| category | Texto | Categoria da equipe |
| gender | Texto | Gênero da equipe |
| age_group | Texto | Faixa etária |
| status | Texto | Situação da equipe no sistema |
| created_at | Data/hora | Data de criação do registro |
| updated_at | Data/hora | Última atualização do registro |

## 👨‍🏫 StaffMember

Representa um membro da comissão técnica ou equipe
multidisciplinar de uma equipe.

### Campos iniciais

| Campo | Tipo conceitual | Descrição |
|---|---|---|
| id | Identificador | Identificador único |
| team_id | Relacionamento | Equipe à qual pertence |
| name | Texto | Nome completo |
| role | Texto | Função exercida na equipe |
| email | Texto | E-mail profissional |
| phone | Texto | Telefone de contato |
| status | Texto | Situação do cadastro |
| created_at | Data/hora | Data de criação |
| updated_at | Data/hora | Última atualização |

## 🏆 Competition

Representa uma competição esportiva e sua temporada.

### Campos iniciais

| Campo | Tipo conceitual | Descrição |
|---|---|---|
| id | Identificador | Identificador único |
| name | Texto | Nome da competição |
| season | Texto | Temporada da competição |
| country | Texto | País ou região |
| organization | Texto | Organização responsável |
| status | Texto | Situação da competição |
| created_at | Data/hora | Data de criação |
| updated_at | Data/hora | Última atualização |

## ⚽ Match

Representa uma partida disputada por uma equipe.

### Campos iniciais

| Campo | Tipo conceitual | Descrição |
|---|---|---|
| id | Identificador | Identificador único da partida |
| team_id | Relacionamento | Equipe que disputou a partida |
| competition_id | Relacionamento | Competição da partida |
| opponent | Texto | Adversário |
| match_date | Data/hora | Data e horário da partida |
| home_away | Texto | Mandante ou visitante |
| stadium | Texto | Local da partida |
| status | Texto | Situação da partida |
| goals_for | Número | Gols marcados pela equipe |
| goals_against | Número | Gols sofridos |
| created_at | Data/hora | Data de criação |
| updated_at | Data/hora | Última atualização |

## 🏋️ TrainingSession

Representa uma sessão de treinamento realizada por uma equipe.

### Campos iniciais

| Campo | Tipo conceitual | Descrição |
|---|---|---|
| id | Identificador | Identificador único |
| team_id | Relacionamento | Equipe que realizou o treino |
| date | Data/hora | Data e horário |
| type | Texto | Tipo de treinamento |
| duration_minutes | Número | Duração planejada ou realizada |
| planned_intensity | Texto | Intensidade planejada |
| description | Texto longo | Descrição do treinamento |
| created_at | Data/hora | Data de criação |
| updated_at | Data/hora | Última atualização |

## 📊 PlayerMatch

Representa a participação e o desempenho de um jogador
em uma determinada partida.

### Campos iniciais

| Campo | Tipo conceitual | Descrição |
|---|---|---|
| id | Identificador | Identificador único |
| match_id | Relacionamento | Partida |
| player_id | Relacionamento | Jogador |
| minutes_played | Número | Minutos jogados |
| goals | Número | Gols marcados |
| assists | Número | Assistências |
| shots | Número | Finalizações |
| passes | Número | Passes registrados |
| tackles | Número | Desarmes |
| rating | Decimal | Nota de desempenho |
| notes | Texto longo | Observações |

## 🏃 TrainingParticipation

Representa a participação individual de um jogador
em uma sessão de treinamento.

### Campos iniciais

| Campo | Tipo conceitual | Descrição |
|---|---|---|
| id | Identificador | Identificador único |
| training_id | Relacionamento | Sessão de treinamento |
| player_id | Relacionamento | Jogador |
| attendance | Booleano | Indica se participou |
| duration_minutes | Número | Minutos realizados |
| rpe | Número | Percepção subjetiva de esforço |
| load | Decimal | Carga calculada |
| notes | Texto longo | Observações |

