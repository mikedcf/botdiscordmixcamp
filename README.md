# MixCamp Discord Bot

Bot do Discord desenvolvido para o MixCamp, oferecendo funcionalidades de gerenciamento de canais e integração com a API do Faceit para buscar informações sobre jogadores, hubs e partidas.

## 📋 Índice

- [Funcionalidades](#funcionalidades)
- [Tecnologias](#tecnologias)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Uso](#uso)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Comandos](#comandos)

## 🚀 Funcionalidades

### Gerenciamento de Canais
- **Criar Canais**: Cria categorias e canais para os times do MixCamp (LEGALIZE e VAC5)
- **Deletar Canais**: Remove categorias e canais dos times

### Integração Faceit
- **Informações de Jogador**: Busca dados completos do perfil de um jogador no Faceit
- **Informações de Hub**: Obtém detalhes sobre uma hub específica
- **Informações de Membro**: Verifica se um jogador é membro de uma hub
- **Informações de Partida**: Busca dados sobre partidas em uma hub

## 🛠️ Tecnologias

- **Python 3.x**
- **discord.py** - Biblioteca para interação com a API do Discord
- **requests** - Para requisições HTTP à API do Faceit
- **python-dotenv** - Gerenciamento de variáveis de ambiente
- **sqlite3** - Banco de dados SQLite

## 📦 Pré-requisitos

- Python 3.8 ou superior
- Conta no Discord Developer Portal
- Token do bot do Discord
- API Key do Faceit

## 🔧 Instalação

1. Clone o repositório ou baixe os arquivos do projeto

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

3. Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:
```env
BotDicord=SEU_TOKEN_DO_BOT_DISCORD
ApiKeyFACEIT=SUA_API_KEY_DO_FACEIT
```

## ⚙️ Configuração

### Criando um Bot no Discord

1. Acesse o [Discord Developer Portal](https://discord.com/developers/applications)
2. Crie uma nova aplicação
3. Vá em "Bot" e crie um bot
4. Copie o token e adicione no arquivo `.env` como `BotDicord`
5. Ative as seguintes permissões no bot:
   - **Privileged Gateway Intents**: 
     - Presence Intent
     - Server Members Intent
     - Message Content Intent
   - **Bot Permissions**:
     - Manage Channels
     - Send Messages
     - View Channels

6. Convide o bot para seu servidor usando o seguinte link (substitua `CLIENT_ID` pelo ID da sua aplicação):
```
https://discord.com/api/oauth2/authorize?client_id=CLIENT_ID&permissions=8&scope=bot%20applications.commands
```

### Obtendo API Key do Faceit

1. Acesse o [Faceit Developer Portal](https://developers.faceit.com/)
2. Crie uma conta ou faça login
3. Crie uma nova aplicação
4. Copie a API Key e adicione no arquivo `.env` como `ApiKeyFACEIT`

### Configurando IDs de Cargos

No arquivo `main.py`, configure os IDs dos cargos que podem usar comandos administrativos:

```python
CEO = 1010316485211738203  # ID do cargo CEO
ADM = 1360721686311338166  # ID do cargo ADM
```

## 🎮 Uso

Execute o bot com:

```bash
python main.py
```

O bot ficará online e responderá aos comandos slash no Discord.

## 📁 Estrutura do Projeto

```
Discord/
│
├── main.py              # Arquivo principal do bot
├── modulos.py           # Módulos com funções auxiliares (Faceit API)
├── requirements.txt     # Dependências do projeto
├── .env                 # Variáveis de ambiente (não versionado)
├── mixcamp.db          # Banco de dados SQLite (gerado automaticamente)
│
└── db/
    └── db.py           # Funções de conexão com o banco de dados
```

## 📝 Comandos

### Comandos Administrativos

#### `/criarcanais`
Cria categorias e canais para os times do MixCamp.
- **Permissão**: Apenas usuários com cargo CEO ou ADM
- **Canais criados**:
  - Categoria: 🎮 LEGALIZE
    - chat-geral (texto)
    - Sala 1 (voz)
  - Categoria: 🎮 VAC5
    - chat-geral (texto)
    - Sala 1 (voz)

#### `/deletarcanais`
Remove todas as categorias e canais dos times.
- **Permissão**: Apenas usuários com cargo CEO ou ADM

### Comandos Faceit

#### `/infoplayerfaceit`
Busca informações completas de um jogador no Faceit.
- **Parâmetros**:
  - `nickname` (string): Nickname do jogador
- **Retorna**:
  - Nível do jogador
  - Faceit ID e Steam ID
  - Nicknames (Faceit e Steam)
  - Link do perfil

#### `/infohub`
Busca informações sobre uma hub do Faceit.
- **Parâmetros**:
  - `hub_uuid` (string): UUID da hub (36 caracteres)
- **Retorna**:
  - Nome, ID e descrição da hub
  - Região e Game ID
  - Total de jogadores
  - Níveis de skill mínimo e máximo
  - Links de avatar e cover image

#### `/infomembrohub`
Verifica se um jogador é membro de uma hub específica.
- **Parâmetros**:
  - `hub_uuid` (string): UUID da hub (36 caracteres)
  - `nickname` (string): Nickname do jogador
- **Retorna**:
  - Status de membro
  - Roles do jogador na hub
  - Link do perfil

#### `/infomatch`
Busca informações sobre partidas em uma hub.
- **Parâmetros**:
  - `match_id` (string): ID da partida (36 caracteres)
- **Retorna**:
  - Nome da hub
  - Match ID
  - Mapas escolhidos
  - Status da partida

#### `/help`
Comando de ajuda (em desenvolvimento).

## 🔒 Segurança

- **Nunca compartilhe** seu arquivo `.env` ou tokens
- Adicione `.env` ao `.gitignore` se versionar o projeto
- Mantenha as permissões do bot no mínimo necessário

## 🐛 Troubleshooting

### Bot não responde aos comandos
- Verifique se o bot está online
- Confirme que os comandos foram sincronizados (o bot faz isso automaticamente no `setup_hook`)
- Verifique as permissões do bot no servidor

### Erro ao buscar informações do Faceit
- Verifique se a API Key está correta no `.env`
- Confirme que a API Key tem as permissões necessárias
- Verifique se o nickname/UUID fornecido está correto

### Erro de permissões
- Confirme que o bot tem permissão para gerenciar canais
- Verifique se os IDs dos cargos CEO e ADM estão corretos

## 📄 Licença

Este projeto é privado e destinado ao uso do MixCamp.

## 👥 Contribuidores

Desenvolvido para o MixCamp.

---

**Nota**: Certifique-se de manter suas credenciais seguras e nunca as compartilhe publicamente.

