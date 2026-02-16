import discord
from discord import app_commands
import os
from discord.ext import commands
from dotenv import load_dotenv
from modulos import buscar_player, hubFaceit, membroHub, MatchFaceit

load_dotenv()

class MixcampBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(
            command_prefix='!',
            intents=intents
        )
        self.tree = app_commands.CommandTree(self)


    async def setup_hook(self):
        await self.tree.sync()


    async def on_ready(self):
        print(f"Bot {self.user} está online!")
bot = MixcampBot()

CEO = 1010316485211738203
ADM = 1360721686311338166


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# ---------- SISTEMA DE CRIAR CANAIS
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

@bot.tree.command(name='help', description='Se precisar de ajuda relacionado ao mixcamp é so perguntar!')

async def teste(interaction: discord.Interaction, sobre: str):
    ...


@bot.tree.command(name="criarcanais", description="Criar canais para os times do MIXCAMP")
@app_commands.checks.has_any_role(CEO, ADM)
async def criar_canais(interaction: discord.Interaction):
    times = ['LEGALIZE', 'VAC5']
    guild = interaction.guild

    if not guild:
        return await interaction.response.send_message("Erro: servidor não encontrado.", ephemeral=True)

    for time in times:
        categoria = await guild.create_category(f"🎮 {time}")
        await guild.create_text_channel("chat-geral", category=categoria)
        await guild.create_voice_channel("Sala 1", category=categoria)

    await interaction.response.send_message("Categorias e canais criados com sucesso!")


@bot.tree.command(name="deletarcanais", description="Deletar canais dos times do MIXCAMP")
@app_commands.checks.has_any_role(CEO, ADM)
async def deletar_canais(interaction: discord.Interaction):
    times = ['LEGALIZE', 'VAC5']
    guild = interaction.guild
    apagou_algo = False

    if not guild:
        return await interaction.response.send_message(
            "Erro: servidor não encontrado.",
            ephemeral=True
        )

    for time in times:
        categoria = discord.utils.get(guild.categories, name=f"🎮 {time}")

        if not categoria:
            continue

        for canal in categoria.channels:
            await canal.delete()

        await categoria.delete()
        apagou_algo = True

    if apagou_algo:
        await interaction.response.send_message(
            "Categorias e canais apagados com sucesso!"
        )
    else:
        await interaction.response.send_message(
            "Nenhuma categoria encontrada."
        )


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# ---------- FACEIT
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# ------ INFO PLAYER FACEIT
@bot.tree.command(name='infoplayerfaceit', description='buscar informações do jogador no Faceit')

async def infoPlayerFaceit(interaction: discord.Interaction, nickname: str):
    player = buscar_player(nickname)
    if player:
        await interaction.response.send_message(f"""
        **Olá {interaction.user.mention}! Aqui está o perfil do jogador:**
        ```
        =-=-=-=-=-=-=-=-🏆 {player['nickFaceit']} | {player['nickSteam']} 🏆=-=-=-=-=-=-=-=-=-=
        📈 Nível: {player['level']}
        🆔 Faceit ID: {player['faceitId']}
        🆔 Steam ID: {player['steamId64']}
        👤 Nickname Faceit: {player['nickFaceit']}
        👤 Nickname Steam: {player['nickSteam']}
        =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
        ```
        🔗 Perfil Faceit: {player['perfilFaceit']}
        """, ephemeral=True)
    else:
        await interaction.response.send_message(f"""
        **Olá {interaction.user.mention}! ❌ Não foi indentificado o Perfil do jogador {nickname}** """, ephemeral=True)


# ------ INFO HUB FACEIT
@bot.tree.command(name='infohub', description='buscar informações da hub na Faceit')

async def infoHub(interaction: discord.Interaction, hub_uuid: str):
    if len(hub_uuid) == 36:
        hub = hubFaceit(hub_uuid)
        if hub:
            await interaction.response.send_message(f"""
            **Olá {interaction.user.mention}! Aqui está as informações da hub:**
            ```
            =-=-=-=-=-=-=-=-🏆 {hub['name']} 🏆=-=-=-=-=-=-=-=-=-=
            🆔 Hub ID: {hub['hubId']}
            🎮 Game ID: {hub['gameId']}
            🌍 Região: {hub['region']}
            📝 Descrição: {hub['description']}
            💬 Chat Room ID: {hub['chatRoomId']}
            👤 Organizador ID: {hub['organizerId']}
            👥🎰 Total de Jogadores: {hub['totalPlayers']}
            🔍 Nível Mínimo ao Máximo: {hub['minSkillLevel']} | {hub['maxSkillLevel']}
            🔍 Permissão de Entrada: {hub['joinPermission']}
            ```
            🖼️*Avatar:* {hub['avatar']}
            🖼️*Cover Image:* {hub['coverImage']}
            🔗*Perfil Faceit:* {hub['faceitUrl']}
            """, ephemeral=True)
        else:
            await interaction.response.send_message(f"""
            **Olá {interaction.user.mention}! ❌ Não foi indentificado a hub {hub_uuid}** """, ephemeral=True)
    else:
        await interaction.response.send_message(f"""
        **Olá {interaction.user.mention}! ❌ A hub não é válida, a hub deve ter 36 caracteres** """, ephemeral=True)


# ------ INFO MEMBRO HUB FACEIT
@bot.tree.command(name='infomembrohub', description='buscar informações do membro da hub na Faceit')

async def infoMembroHub(interaction: discord.Interaction, hub_uuid: str, nickname: str):
    if len(hub_uuid) == 36:
        membro = membroHub(hub_uuid, nickname)
        if membro['status']:
            await interaction.response.send_message(f"""
            **Olá {interaction.user.mention}! ✅Membro localizado na hub, informações abaixo:**
            ```
            =-=-=-=-=-=-=-=-🏆 {membro['data']['nickname']} 🏆=-=-=-=-=-=-=-=-=-=
            👥 Roles: {membro['data']['roles']}
            =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
            ```
            🔗 **Perfil Faceit:** {membro['data']['faceit_url']}
            """, ephemeral=True)
        else:

           await interaction.response.send_message(f"""
           **Olá {interaction.user.mention}! ❌{membro['mensagem']}** """, ephemeral=True)
        
    else:
        await interaction.response.send_message(f"""
        **Olá {interaction.user.mention}! ❌ A hub não é válida, a hub deve ter 36 caracteres ou o membro não foi encontrado na hub {hub_uuid}** """, ephemeral=True)



# ------ INFO MATCH HUB FACEIT
@bot.tree.command(name='infomatch', description='buscar informações da partida na Faceit')

async def infoMatch(interaction: discord.Interaction, match_id: str):
    if len(match_id) == 36:
        match = MatchFaceit(match_id)
        print(match)
        if match['status']:
            await interaction.response.send_message(f"""
            **Olá {interaction.user.mention}! ✅ Partida localizada, informações abaixo:**
            ```
            =-=-=-=-=-=-=-=-🏆 {match['dados']['nomeHub']} 🏆=-=-=-=-=-=-=-=-=-=
            🆔 Match ID: {match['dados']['matchId']}
            🎮 Mapas: {match['dados']['mapas']}
            🔍 MD: {match['dados']['md']}
            🔍 Status: {match['dados']['status']}
            ```
            """, ephemeral=True)
        else:
            await interaction.response.send_message(f"""
            **Olá {interaction.user.mention}! ❌{match['mensagem']}** """, ephemeral=True)
        
        
    else:
        await interaction.response.send_message(f"""
        **Olá {interaction.user.mention}! ❌ A hub não é válida, a hub deve ter 36 caracteres ou o membro não foi encontrado na hub ** """, ephemeral=True)

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# ---------- MIXCAMP
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# ---------- START BOT
if __name__ == "__main__":
    bot.run(os.getenv("BotDicord"))