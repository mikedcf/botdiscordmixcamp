# MixCamp Discord Bot

Bot do Discord desenvolvido para o **MixCamp**, integrando o servidor da comunidade com o site e a API do MixCamp, além da API do Faceit. Oferece vinculação de contas, perfis, tickets de suporte, agendamento de partidas, gerenciamento de cargos/canais e ferramentas administrativas.

## Índice

- [Funcionalidades](#funcionalidades)
- [Tecnologias](#tecnologias)
- [Pré-requisitos](#pré-requisitos)
- [Instalação](#instalação)
- [Configuração](#configuração)
- [Primeira execução](#primeira-execução)
- [Uso](#uso)
- [Estrutura do Projeto](#estrutura-do-projeto)
- [Comandos](#comandos)
- [Banco de Dados](#banco-de-dados)
- [Segurança](#segurança)
- [Troubleshooting](#troubleshooting)

## Funcionalidades

### Integração com o MixCamp
- **Vinculação de conta**: painel com botão/modal para o usuário enviar o link do perfil no site
- **Sincronização de perfil**: atualiza nickname, cargos de time e cargo de verificado com base nos dados da API
- **Painel de perfil**: botão para atualizar informações exibidas no Discord após mudanças no site
- **Consulta de jogador**: busca dados completos de um player cadastrado no MixCamp (staff)
- **Cargos de times**: cria cargos automaticamente com base nos times registrados no site
- **Agendamento de partidas**: painel interativo para marcar confrontos entre equipes
- **Listagem de agendamentos**: exibe partidas de hoje, da semana ou todas as próximas

### Sistema de suporte
- **Tickets**: categorias, canais e painel com opções (bug, report, técnico, sugestão, dúvidas)
- **Canais administrativos**: logs, solicitações, chat staff, chegou/vazou, reunião em voz
- **Webhooks**: notificações automáticas em canais configurados

### Gerenciamento do servidor
- **Configuração base**: cria e registra cargos essenciais (STAFF, MODERADOR, Verificado, STREAMER, PASSE-LIVRE)
- **Estrutura completa**: comando para montar categorias de boas-vindas, suporte e área staff
- **Canais de times**: cria/remove categorias e canais para times específicos (LEGALIZE e VAC5)

### Ferramentas extras
- **MIX amistoso**: sorteia aleatoriamente 10 jogadores entre dois times informados
- **Integração Faceit**: consulta de jogador, hub, membro de hub e partida

## Tecnologias

- **Python 3.8+**
- **discord.py** — interação com a API do Discord (slash commands, views, modals)
- **requests** — requisições HTTP síncronas (Faceit e MixCamp)
- **aiohttp** — requisições HTTP assíncronas
- **python-dotenv** — variáveis de ambiente
- **SQLite** — persistência local (`db/sql/mixcamp.db`)

## Pré-requisitos

- Python 3.8 ou superior
- Conta no [Discord Developer Portal](https://discord.com/developers/applications)
- Token do bot do Discord
- API Key do Faceit
- API Key do MixCamp e URLs das rotas da API (backend do site)

## Instalação

1. Clone o repositório ou baixe os arquivos do projeto.

2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Crie um arquivo `.env` na raiz do projeto (veja [Configuração](#configuração)).

4. Garanta que o diretório `db/sql/` exista. O banco `mixcamp.db` é criado/usado automaticamente pelo bot.

## Configuração

### Variáveis de ambiente (`.env`)

```env
# Discord
BotDicord=SEU_TOKEN_DO_BOT_DISCORD

# Faceit
ApiKeyFACEIT=SUA_API_KEY_DO_FACEIT

# MixCamp
ApiKeyMIXCAMP=SUA_API_KEY_DO_MIXCAMP

# Webhooks e rotas da API MixCamp
ROUTE_PERFIL_WEHOOK=URL_DO_WEBHOOK_PERFIL
ROUTE_MIXCAMP_API_TIMES=URL_DA_API_DE_TIMES
ROUTE_MIXCAMP_API_PERFIL=URL_DA_API_DE_PERFIL
ROUTE_MIXCAMP_API_USER_COMPLETO=URL_DA_API_USER_COMPLETO
ROUTE_MIXCAMP_API_SEASONS=URL_DA_API_SEASONS
ROUTE_MIXCAMP_API_AGENDAMENTOS=URL_DA_API_AGENDAMENTOS
ROUTE_MIXCAMP_API_USERS_ALL=URL_DA_API_USERS
ROUTE_MARCACOES_JOGOS_CRIAR=URL_DA_API_CRIAR_AGENDAMENTO
```

> O arquivo `.env` já está listado no `.gitignore` e **não deve ser versionado**.

### Criando um bot no Discord

1. Acesse o [Discord Developer Portal](https://discord.com/developers/applications)
2. Crie uma nova aplicação e, em **Bot**, gere o token
3. Adicione o token no `.env` como `BotDicord`
4. Ative os **Privileged Gateway Intents**:
   - Presence Intent
   - Server Members Intent
   - Message Content Intent
5. Conceda permissões ao bot, no mínimo:
   - Manage Channels
   - Manage Roles
   - Send Messages
   - View Channels
   - Manage Nicknames

6. Convide o bot para o servidor (substitua `CLIENT_ID`):

```
https://discord.com/api/oauth2/authorize?client_id=CLIENT_ID&permissions=8&scope=bot%20applications.commands
```

### Obtendo API Key do Faceit

1. Acesse o [Faceit Developer Portal](https://developers.faceit.com/)
2. Crie uma aplicação e copie a API Key
3. Adicione no `.env` como `ApiKeyFACEIT`

### Cargos e permissões internas

Os IDs de cargos administrativos (**OWNER**, **STAFF**, **MODERADOR**, **Verificado**) são armazenados no banco SQLite após executar `/configbase`. Não é necessário editar IDs manualmente no código — o bot carrega esses valores automaticamente no `on_ready`.

O usuário que executa `/configbase` precisa possuir um cargo cujo nome contenha `OWNER` (padrão: `'👑┇OWNER`).

## Primeira execução

Ordem recomendada para configurar um servidor novo:

| Passo | Comando | Quem executa |
|-------|---------|--------------|
| 1 | `/createtables` | OWNER |
| 2 | `/configbase` | OWNER |
| 3 | `/criarlocaladm` | Staff (OWNER/STAFF/MODERADOR) |
| 4 | `/painel_link` | Qualquer usuário (postar no canal de identificação) |
| 5 | `/carregartime` | STAFF/OWNER (sincronizar cargos de times) |
| 6 | `/painelagendamento` | Staff (postar painel de agendamento) |

## Uso

Execute o bot:

```bash
python main.py
```

O bot sincroniza os slash commands no `setup_hook` e permanece online aguardando interações (comandos, botões e modals).

## Estrutura do Projeto

```
Discord/
│
├── main.py              # Bot principal: eventos, views, modals e slash commands
├── modulos.py           # Faceit API, MixCamp API, funções de banco e utilitários
├── requirements.txt     # Dependências Python
├── .env                 # Variáveis de ambiente (não versionado)
├── .gitignore
│
└── db/
    ├── db.py            # Conexão SQLite
    └── sql/
        └── mixcamp.db   # Banco de dados local (não versionado)
```

## Comandos

### Configuração e administração

| Comando | Descrição | Permissão |
|---------|-----------|-----------|
| `/configbase` | Cria cargos base e registra IDs no banco | Cargo OWNER |
| `/createtables` | Cria tabelas SQLite | OWNER |
| `/criarlocaladm` | Monta categorias, canais, webhooks e painéis (tickets, perfil, staff) | Staff |
| `/carregartime` | Cria cargos de times com base na API do MixCamp | OWNER / STAFF |
| `/criarcanais` | Cria categorias e canais para LEGALIZE e VAC5 | OWNER / STAFF |
| `/deletarcanais` | Remove categorias e canais dos times acima | OWNER / STAFF |

### Comunidade e perfil

| Comando | Descrição | Permissão |
|---------|-----------|-----------|
| `/painel_link` | Envia embed com botão para vincular conta do site | Público |
| `/painelagendamento` | Abre painel interativo para agendar partidas | Staff |
| `/veragendamentos` | Lista partidas (hoje / semana / todas) | Público |
| `/mix` | Sorteia 10 jogadores entre dois times | Público |
| `/help` | Comando de ajuda (utilitário interno) | Público |

### MixCamp

| Comando | Parâmetros | Descrição | Permissão |
|---------|------------|-----------|-----------|
| `/infoplayermix` | `nickname` | Dados completos do player no MixCamp | OWNER / STAFF |

### Faceit

| Comando | Parâmetros | Descrição |
|---------|------------|-----------|
| `/infoplayerfaceit` | `nickname` | Perfil do jogador (nível, IDs, nicknames) |
| `/infohub` | `hub_uuid` | Informações de uma hub (UUID com 36 caracteres) |
| `/infomembrohub` | `hub_uuid`, `nickname` | Verifica membro e roles na hub |
| `/infomatch` | `match_id` | Dados de uma partida (UUID com 36 caracteres) |

### Interações persistentes (botões e modals)

Além dos slash commands, o bot registra views persistentes no `on_ready`:

- **LinkView / LinkModal** — vinculação de perfil do site
- **PainelPerfilView** — atualização de perfil no Discord
- **PainelAgendamento / ModalAgendarJogo** — agendamento de confrontos
- **TicketView / TicketModal / CloseTicketView** — abertura e fechamento de tickets

## Banco de Dados

O SQLite armazena três tabelas principais (criadas via `/createtables`):

| Tabela | Finalidade |
|--------|------------|
| `usuarios_discord` | Vínculo Discord ↔ MixCamp, dados de time e perfil |
| `sistema_discord` | IDs de cargos, canais, categorias e URLs de webhooks |
| `tickets` | Registro de tickets abertos (tipo, status, canal, etc.) |

Arquivo: `db/sql/mixcamp.db`

## Segurança

- **Nunca compartilhe** o arquivo `.env`, tokens ou API keys
- O `.env` e `db/sql/` já estão no `.gitignore`
- Conceda ao bot apenas as permissões necessárias
- O comando `/infoplayermix` expõe dados sensíveis (e-mail, IDs) — restrito a staff

## Troubleshooting

### Bot não responde aos comandos
- Confirme que o bot está online
- Verifique se os comandos foram sincronizados (ocorre automaticamente no startup)
- Cheque permissões do bot no servidor

### Erro ao vincular perfil ou buscar dados do MixCamp
- Valide `ApiKeyMIXCAMP` e todas as variáveis `ROUTE_MIXCAMP_*` no `.env`
- Confirme que a API do site está acessível
- Execute `/createtables` e `/configbase` antes de usar painéis

### Erro ao buscar informações do Faceit
- Verifique `ApiKeyFACEIT` no `.env`
- Confirme nickname/UUID informados

### Cargos ou canais não funcionam
- Execute `/configbase` e `/criarlocaladm` na ordem correta
- Confirme que o bot tem permissão para **Manage Channels** e **Manage Roles**
- Use `/carregartime` para sincronizar cargos de times após alterações no site

### Permissão negada em comandos administrativos
- Os cargos OWNER/STAFF/MODERADOR são lidos do banco — rode `/configbase` primeiro
- Reinicie o bot após alterações nos cargos registrados

## Licença

Projeto privado, destinado ao uso do MixCamp.

## Contribuidores

Desenvolvido para o MixCamp.

---

**Nota:** Mantenha credenciais e chaves de API seguras. Nunca as publique em repositórios públicos.
