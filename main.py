import discord
import requests
import asyncio
import aiohttp
import os
from time import sleep
from datetime import datetime
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from modulos import *
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

bot = MixcampBot()

CEO = None
STAFF = None
MODERADOR = None
STREAMER = None
VERIFICADO = None
CATEGORIATICKETID = None
criarTableDb()

@bot.event
async def on_ready():
    global CEO, STAFF, MODERADOR, VERIFICADO, CATEGORIATICKETID, STREAMER
    
    verificarExiste = getDadosSistema('owner')
    if verificarExiste['status']:
        CEO = verificarExiste['data']['id_tipo']


    verificarExiste = getDadosSistema('staff')
    if verificarExiste['status']:
        STAFF = verificarExiste['data']['id_tipo']

    verificarExiste = getDadosSistema('moderador')
    if verificarExiste['status']:
        MODERADOR = verificarExiste['data']['id_tipo']

    verificarExiste = getDadosSistema('verificado')
    if verificarExiste['status']:
        VERIFICADO = verificarExiste['data']['id_tipo']

    verificarExiste = getDadosSistema('streamer')
    if verificarExiste['status']:
        STREAMER = verificarExiste['data']['id_tipo']

    verificarExiste = getDadosSistema('ca-suport')
    if verificarExiste['status']:
        CATEGORIATICKETID = verificarExiste['data']['id_tipo']

    

    

    bot.add_view(TicketView())
    bot.add_view(CloseTicketView())
    bot.add_view(LinkModal())
    bot.add_view(LinkView())
    bot.add_view(PainelPerfilView())
    bot.add_view(PainelAgendamento())


    await bot.tree.sync()


    print(f"Bot online como {bot.user}")

async def AtualizarIdCargos():
    global CEO, STAFF, MODERADOR, VERIFICADO, CATEGORIATICKETID, STREAMER
    
    verificarExiste = getDadosSistema('owner')
    if verificarExiste['status']:
        CEO = verificarExiste['data']['id_tipo']


    verificarExiste = getDadosSistema('staff')
    if verificarExiste['status']:
        STAFF = verificarExiste['data']['id_tipo']

    verificarExiste = getDadosSistema('moderador')
    if verificarExiste['status']:
        MODERADOR = verificarExiste['data']['id_tipo']

    verificarExiste = getDadosSistema('verificado')
    if verificarExiste['status']:
        VERIFICADO = verificarExiste['data']['id_tipo']

    verificarExiste = getDadosSistema('ca-suport')
    if verificarExiste['status']:
        CATEGORIATICKETID = verificarExiste['data']['id_tipo']

    verificarExiste = getDadosSistema('streamer')
    if verificarExiste['status']:
        STREAMER = verificarExiste['data']['id_tipo']

async def adicionar_cargo(membro, guild, id_cargo):
    if id_cargo is None:
        return
    cargo = guild.get_role(id_cargo)
    if cargo:
        await membro.add_roles(cargo)

def check_staff():
    async def predicate(interaction: discord.Interaction):
        global CEO, STAFF

        if CEO is None or STAFF is None or MODERADOR is None or STREAMER is None:
            return False

        roles_user = [role.id for role in interaction.user.roles]

        return CEO in roles_user or STAFF in roles_user or MODERADOR in roles_user or STREAMER in roles_user

    return app_commands.check(predicate)

async def AtualizarCargoTimes(guild):
    timesMixcamp = GetTimes()
    times = []
    cargosDiscord = []

    for time in timesMixcamp:
        times.append(time.lower())
    

    for roles in guild.roles:
        if roles.name == '@everyone':
            pass
        else:
            CargoTimeRole = roles.name.split('┇')[1].strip().lower()
            cargosDiscord.append(CargoTimeRole)

    for time in times:
        if time not in cargosDiscord:
            await guild.create_role(
            name=f'.🥋┇ {time.upper()}',
            colour=discord.Colour.blue(),
            hoist=True,
            mentionable=True
        )

    webhook_url = getDadosSistema('c-logs')['data']['webhook_url']
    
    data = {
        "content": "✅ **Cargos de times carregados com sucesso!**"
    }
    requests.post(webhook_url, json=data)
           
async def MostrarOuAtualizarPerfil(interaction: discord.Interaction):

    
    #1- puxar o id do usuario do discord do inetraction
    userDiscordID = interaction.user.id
    #2- puxar o dados do desse usuario no banco de dados do sql lite e comparar se existe
    dadosUserDiscord = getDadosUserDiscord(userDiscordID)
    idUserDiscord = dadosUserDiscord['data']['userdiscordid']
    if dadosUserDiscord['status']:
        idMixcamp = dadosUserDiscord['data']['usermixcampid']
        timeIdDiscord = dadosUserDiscord['data']['time_id']

        dadosUserCompleto = getDadosUserCompleto(idMixcamp)
        if dadosUserCompleto['status']:
            timeIdMixcamp = dadosUserCompleto['data']['userDados'][0]['time_id']

            username = dadosUserCompleto['data']['userDados'][0]['username']
            email = dadosUserCompleto['data']['userDados'][0]['email']
            steamid = dadosUserCompleto['data']['userDados'][0]['steamid']
            faceitid = dadosUserCompleto['data']['userDados'][0]['faceitid']
            avatar_url = dadosUserCompleto['data']['userDados'][0]['avatar_url']
            posicoes = dadosUserCompleto['data']['userDados'][0]['posicoes']
            gerencia = dadosUserCompleto['data']['userDados'][0]['gerencia']
            organizador = dadosUserCompleto['data']['userDados'][0]['organizador']
            cores_perfil = dadosUserCompleto['data']['userDados'][0]['cores_perfil']
            cores_perfil = cores_perfil[:7]
            link_cfg = dadosUserCompleto['data']['userDados'][0]['cfg_cs']
            discord_url = dadosUserCompleto['data']['userDados'][0]['discord_url']
            youtube_url = dadosUserCompleto['data']['userDados'][0]['youtube_url']
            instagram_url = dadosUserCompleto['data']['userDados'][0]['instagram_url']
            twitter_url = dadosUserCompleto['data']['userDados'][0]['twitter_url']
            twitch_url = dadosUserCompleto['data']['userDados'][0]['twitch_url']
            faceit_url = dadosUserCompleto['data']['userDados'][0]['faceit_url']
            gamesclub_url = dadosUserCompleto['data']['userDados'][0]['gamesclub_url']
            steam_url = dadosUserCompleto['data']['userDados'][0]['steam_url']
            tiktok_url = dadosUserCompleto['data']['userDados'][0]['tiktok_url']
            kick_url = dadosUserCompleto['data']['userDados'][0]['kick_url']
            allstar_url = dadosUserCompleto['data']['userDados'][0]['allstar_url']
            total_medalhas = dadosUserCompleto['data']['userDados'][0]['total_medalhas']
            total_destaques = dadosUserCompleto['data']['userDados'][0]['total_destaques']

            if gerencia == 'streammer':
                gerencia = 'streamer'

            if timeIdMixcamp is not None:
                nomeDoTimeNovo = dadosUserCompleto['data']['userDados'][0]['nome_time'].lower().strip()
                if nomeDoTimeNovo is not None:
                    pass
                else:
                    nomeDoTimeAntigo = dadosUserDiscord['data'][11].strip().lower()
                
                if timeIdMixcamp is not None or timeIdDiscord is not None:

                    if timeIdMixcamp != timeIdDiscord:

                        for roles in interaction.guild.roles:
                            if roles.name == '@everyone':
                                pass
                            else:
                                if nomeDoTimeNovo is not None:
                                    pass
                                else:
                                    cargoNome = roles.name.split('┇')[1].strip().lower()
                                    if cargoNome == nomeDoTimeAntigo:
                                        await interaction.user.remove_roles(roles)
                                        break

                        for roles in interaction.guild.roles:
                            if roles.name == '@everyone':
                                pass
                            else:
                                cargoNome = roles.name.split('┇')[1].strip().lower()
                                if cargoNome == nomeDoTimeNovo:
                                    await interaction.user.add_roles(roles)
                                    #DADOS DO MIXCAMP ATUALIZADOS
                                    tag_time = dadosUserCompleto['data']['userDados'][0]['tag_time']
                                    lider_id = dadosUserCompleto['data']['userDados'][0]['lider_id']
                                    avatar_time_url = dadosUserCompleto['data']['userDados'][0]['avatar_time_url']
                                    funcao_no_time = dadosUserCompleto['data']['userDados'][0]['funcao']
                                    posicao_no_time = dadosUserCompleto['data']['userDados'][0]['posicao']
                                    total_membros = dadosUserCompleto['data']['userDados'][0]['total_membros']
                                    total_conquistas_time = dadosUserCompleto['data']['userDados'][0]['total_conquistas_time']

                                    

                                    embed = discord.Embed(
                                        title=f"`👤` {username} • Perfil Competitivo",
                                        description=(
                                            f"`🏆` Perfil competitivo MIXCAMP\n"
                                            f"`🎮` Jogador competitivo de CS2"
                                        ),
                                        color=discord.Color.from_str(cores_perfil)
                                    )

                                    # =========================================================
                                    # AUTHOR / THUMBNAIL
                                    # =========================================================

                                    embed.set_author(
                                        name=f"{username} • {tag_time}",
                                        icon_url=avatar_time_url
                                    )

                                    embed.set_thumbnail(url=avatar_url)

                                    # =========================================================
                                    # DADOS GERAIS
                                    # =========================================================

                                    embed.add_field(
                                        name="`🆔` Informações Gerais",
                                        value=(
                                            f"`🆔` ID: `{idMixcamp}`\n"
                                            f"`👤` Username: `{username}`\n"
                                            f"`📧` Email: `{email}`\n"
                                            f"`🛡️` Gerência: `{gerencia}`\n"
                                            f"`💎` Organizador: `{organizador}`"
                                        ),
                                        inline=False
                                    )

                                    # =========================================================
                                    # COMPETITIVO
                                    # =========================================================

                                    embed.add_field(
                                        name="`🎮` Competitivo",
                                        value=(
                                            f"`🚂` SteamID: `{steamid}`\n"
                                            f"`🎯` FACEIT ID: `{faceitid}`\n"
                                            f"`🎖️` Função: `{funcao_no_time}`\n"
                                            f"`📍` Posição Principal: `{posicao_no_time}`"
                                        ),
                                        inline=False
                                    )

                                    # =========================================================
                                    # TIME
                                    # =========================================================

                                    embed.add_field(
                                        name="`👥` Time",
                                        value=(
                                            f"`🆔` ID: `{timeIdMixcamp}`\n"
                                            f"`🏷️` Nome: `{nomeDoTimeNovo}`\n"
                                            f"`🏷️` Tag: `{tag_time}`\n"
                                            f"`👑` Líder ID: `{lider_id}`\n"
                                            f"`👥` Total de membros: `{total_membros}`\n"
                                            f"`🏆` Conquistas: `{total_conquistas_time}`"
                                        ),
                                        inline=False
                                    )

                                    # =========================================================
                                    # ESTATISTICAS
                                    # =========================================================

                                    embed.add_field(
                                        name="`📊` Estatísticas",
                                        value=(
                                            f"`🏅` Medalhas: `{total_medalhas}`\n"
                                            f"`🎬` Destaques: `{total_destaques}`"
                                        ),
                                        inline=True
                                    )

                                    # =========================================================
                                    # POSIÇÕES
                                    # =========================================================

                                    embed.add_field(
                                        name="`🎯` Roles",
                                        value=f"```{posicoes}```",
                                        inline=True
                                    )

                                    # =========================================================
                                    # REDES SOCIAIS
                                    # =========================================================

                                    redes = []

                                    if discord_url:
                                        redes.append(f"[Discord]({discord_url})")

                                    if twitter_url:
                                        redes.append(f"[Twitter]({twitter_url})")

                                    if instagram_url:
                                        redes.append(f"[Instagram]({instagram_url})")

                                    if youtube_url:
                                        redes.append(f"[YouTube]({youtube_url})")

                                    if twitch_url:
                                        redes.append(f"[Twitch]({twitch_url})")

                                    if faceit_url:
                                        redes.append(f"[FACEIT]({faceit_url})")

                                    if gamesclub_url:
                                        redes.append(f"[GamersClub]({gamesclub_url})")

                                    if steam_url:
                                        redes.append(f"[Steam]({steam_url})")

                                    if tiktok_url:
                                        redes.append(f"[TikTok]({tiktok_url})")

                                    if kick_url:
                                        redes.append(f"[Kick]({kick_url})")

                                    if allstar_url:
                                        redes.append(f"[AllStar]({allstar_url})")

                                    embed.add_field(
                                        name="`🌐` Redes Sociais",
                                        value=" • ".join(redes),
                                        inline=False
                                    )

                                    # =========================================================
                                    # CFG
                                    # =========================================================

                                    if link_cfg:
                                        embed.add_field(
                                            name="`⚙️` CFG CS2",
                                            value=f"[📥 Download CFG]({link_cfg})",
                                            inline=False
                                        )

                                    # =========================================================
                                    # FOOTER
                                    # =========================================================

                                    embed.set_footer(
                                        text=f"MIXCAMP • USER ID {dadosUserCompleto['data']['userDados'][0]['id']}"
                                    )

                                    await interaction.followup.send(
                                        embed=embed,
                                        ephemeral=True
                                    )

                                    novoApelido = f'｢{tag_time}｣'
                                    await interaction.user.edit(nick=f"")

                                    if steamid is not None or faceitid is not None:
                                        novoApelido = '✔'+novoApelido

                                    

                                    if idMixcamp == lider_id:
                                        novoApelido = novoApelido + '👑'
                                    
                                    if funcao_no_time == 'Coach':
                                        novoApelido = novoApelido + '🎧'

                                    if gerencia == 'admin':
                                        novoApelido = novoApelido +'⚙️'
                                        await adicionar_cargo(interaction.user, interaction.guild, STAFF)
                                    elif gerencia == 'moderador':
                                        novoApelido = novoApelido +'🛡️'
                                        await adicionar_cargo(interaction.user, interaction.guild, MODERADOR)
                                    elif gerencia == 'streamer':
                                        novoApelido = novoApelido + '🎥'
                                        await adicionar_cargo(interaction.user, interaction.guild, STREAMER)

                                    if organizador == 'premium':
                                        novoApelido = novoApelido + '🏆'

                                    elif organizador == 'simples':
                                        novoApelido = novoApelido + '🥇'


                                    await interaction.user.edit(nick=f"{novoApelido}┇{username}")

                                    atualiiarDadosUserDiscord('time_id',timeIdMixcamp,idUserDiscord)
                                    atualiiarDadosUserDiscord('lider_id',lider_id,idUserDiscord)
                                    atualiiarDadosUserDiscord('nome_time',nomeDoTimeNovo,idUserDiscord)
                                    atualiiarDadosUserDiscord('tag_time',tag_time,idUserDiscord)
                                    atualiiarDadosUserDiscord('avatar_time_url',avatar_time_url,idUserDiscord)
                                    atualiiarDadosUserDiscord('funcao_no_time',funcao_no_time,idUserDiscord)
                                    atualiiarDadosUserDiscord('posicao_no_time',posicao_no_time,idUserDiscord)

                                    if username != dadosUserDiscord['data']['username']:
                                        atualiiarDadosUserDiscord('username',username,idUserDiscord)

                                    if steamid != dadosUserDiscord['data']['steamid']:
                                        atualiiarDadosUserDiscord('steamid',steamid,idUserDiscord)

                                    if faceitid != dadosUserDiscord['data']['faceitid']:
                                        atualiiarDadosUserDiscord('faceitid',faceitid,idUserDiscord)

                                    if avatar_url != dadosUserDiscord['data']['avatar_url']:
                                        atualiiarDadosUserDiscord('avatar_url',avatar_url,idUserDiscord)

                                    if gerencia != dadosUserDiscord['data']['gerencia']:
                                        atualiiarDadosUserDiscord('gerencia',gerencia,idUserDiscord)

                                    if organizador != dadosUserDiscord['data']['organizador']:
                                        atualiiarDadosUserDiscord('organizador',organizador,idUserDiscord)

                                    break
                    else:

                        tag_time = dadosUserCompleto['data']['userDados'][0]['tag_time']
                        lider_id = dadosUserCompleto['data']['userDados'][0]['lider_id']
                        avatar_time_url = dadosUserCompleto['data']['userDados'][0]['avatar_time_url']
                        funcao_no_time = dadosUserCompleto['data']['userDados'][0]['funcao']
                        posicao_no_time = dadosUserCompleto['data']['userDados'][0]['posicao']
                        total_membros = dadosUserCompleto['data']['userDados'][0]['total_membros']
                        total_conquistas_time = dadosUserCompleto['data']['userDados'][0]['total_conquistas_time']

                        embed = discord.Embed(
                            title=f"`👤` {username} • Perfil Competitivo",
                            description=(
                                f"`🏆` Perfil competitivo MIXCAMP\n"
                                f"`🎮` Jogador competitivo de CS2"
                            ),
                            color=discord.Color.from_str(cores_perfil)
                        )

                        # =========================================================
                        # AUTHOR / THUMBNAIL
                        # =========================================================

                        embed.set_author(
                            name=f"{username} • {tag_time}",
                            icon_url=avatar_time_url
                        )

                        embed.set_thumbnail(url=avatar_url)

                        # =========================================================
                        # DADOS GERAIS
                        # =========================================================

                        embed.add_field(
                            name="`🆔` Informações Gerais",
                            value=(
                                f"`🆔` ID: `{idMixcamp}`\n"
                                f"`👤` Username: `{username}`\n"
                                f"`📧` Email: `{email}`\n"
                                f"`🛡️` Gerência: `{gerencia}`\n"
                                f"`💎` Organizador: `{organizador}`"
                            ),
                            inline=False
                        )

                        # =========================================================
                        # COMPETITIVO
                        # =========================================================

                        embed.add_field(
                            name="`🎮` Competitivo",
                            value=(
                                f"`🚂` SteamID: `{steamid}`\n"
                                f"`🎯` FACEIT ID: `{faceitid}`\n"
                                f"`🎖️` Função: `{funcao_no_time}`\n"
                                f"`📍` Posição Principal: `{posicao_no_time}`"
                            ),
                            inline=False
                        )

                        # =========================================================
                        # TIME
                        # =========================================================

                        embed.add_field(
                            name="`👥` Time",
                            value=(
                                f"`🆔` ID: `{timeIdMixcamp}`\n"
                                f"🏷️ Nome: `{nomeDoTimeNovo}`\n"
                                f"`🏷️` Tag: `{tag_time}`\n"
                                f"`👑` Líder ID: `{lider_id}`\n"
                                f"`👥` Total de membros: `{total_membros}`\n"
                                f"`🏆` Conquistas: `{total_conquistas_time}`"
                            ),
                            inline=False
                        )

                        # =========================================================
                        # ESTATISTICAS
                        # =========================================================

                        embed.add_field(
                            name="`📊` Estatísticas",
                            value=(
                                f"`🏅` Medalhas: `{total_medalhas}`\n"
                                f"`🎬` Destaques: `{total_destaques}`"
                            ),
                            inline=True
                        )

                        # =========================================================
                        # POSIÇÕES
                        # =========================================================

                        embed.add_field(
                            name="`🎯` Roles",
                            value=f"```{posicoes}```",
                            inline=True
                        )

                        # =========================================================
                        # REDES SOCIAIS
                        # =========================================================

                        redes = []

                        if discord_url:
                            redes.append(f"[Discord]({discord_url})")

                        if twitter_url:
                            redes.append(f"[Twitter]({twitter_url})")

                        if instagram_url:
                            redes.append(f"[Instagram]({instagram_url})")

                        if youtube_url:
                            redes.append(f"[YouTube]({youtube_url})")

                        if twitch_url:
                            redes.append(f"[Twitch]({twitch_url})")

                        if faceit_url:
                            redes.append(f"[FACEIT]({faceit_url})")

                        if gamesclub_url:
                            redes.append(f"[GamersClub]({gamesclub_url})")

                        if steam_url:
                            redes.append(f"[Steam]({steam_url})")

                        if tiktok_url:
                            redes.append(f"[TikTok]({tiktok_url})")

                        if kick_url:
                            redes.append(f"[Kick]({kick_url})")

                        if allstar_url:
                            redes.append(f"[AllStar]({allstar_url})")

                        embed.add_field(
                            name="`🌐` Redes Sociais",
                            value=" • ".join(redes),
                            inline=False
                        )

                        # =========================================================
                        # CFG
                        # =========================================================

                        if link_cfg:
                            embed.add_field(
                                name="`⚙️` CFG CS2",
                                value=f"[📥 Download CFG]({link_cfg})",
                                inline=False
                            )

                        # =========================================================
                        # FOOTER
                        # =========================================================

                        embed.set_footer(
                            text=f"MIXCAMP • USER ID {dadosUserCompleto['data']['userDados'][0]['id']}"
                        )

                        await interaction.followup.send(
                            embed=embed,
                            ephemeral=True
                        )

                        novoApelido = f'｢{tag_time}｣'
                        await interaction.user.edit(nick=f"")

                        if steamid is not None or faceitid is not None:
                            novoApelido = '✔'+novoApelido

                        

                        if idMixcamp == lider_id:
                            novoApelido = novoApelido + '👑'
                        
                        if funcao_no_time == 'Coach':
                            novoApelido = novoApelido + '🎧'

                        if gerencia == 'admin':
                            novoApelido = novoApelido +'⚙️'
                            await adicionar_cargo(interaction.user, interaction.guild, STAFF)
                        elif gerencia == 'moderador':
                            novoApelido = novoApelido +'🛡️'
                            await adicionar_cargo(interaction.user, interaction.guild, MODERADOR)
                        elif gerencia == 'streamer':
                            novoApelido = novoApelido + '🎥'
                            await adicionar_cargo(interaction.user, interaction.guild, STREAMER)
                        if organizador == 'premium':
                            novoApelido = novoApelido + '🏆'

                        elif organizador == 'simples':
                            novoApelido = novoApelido + '🥇'


                        await interaction.user.edit(nick=f"{novoApelido}┇{username}")


                        if username != dadosUserDiscord['data']['username']:
                            atualiiarDadosUserDiscord('username',username,idUserDiscord)

                        if steamid != dadosUserDiscord['data']['steamid']:
                            atualiiarDadosUserDiscord('steamid',steamid,idUserDiscord)

                        if faceitid != dadosUserDiscord['data']['faceitid']:
                            atualiiarDadosUserDiscord('faceitid',faceitid,idUserDiscord)

                        if avatar_url != dadosUserDiscord['data']['avatar_url']:
                            atualiiarDadosUserDiscord('avatar_url',avatar_url,idUserDiscord)

                        if gerencia != dadosUserDiscord['data']['gerencia']:
                            atualiiarDadosUserDiscord('gerencia',gerencia,idUserDiscord)

                        if organizador != dadosUserDiscord['data']['organizador']:
                            atualiiarDadosUserDiscord('organizador',organizador,idUserDiscord)

                        if timeIdMixcamp != dadosUserDiscord['data']['time_id']:
                            atualiiarDadosUserDiscord('time_id',timeIdMixcamp,idUserDiscord)

                        if lider_id != dadosUserDiscord['data']['lider_id']:
                            atualiiarDadosUserDiscord('lider_id',lider_id,idUserDiscord)

                        if nomeDoTimeNovo != dadosUserDiscord['data']['nome_time']:
                            atualiiarDadosUserDiscord('nome_time',nomeDoTimeNovo,idUserDiscord)

                        if tag_time != dadosUserDiscord['data']['tag_time']:
                            atualiiarDadosUserDiscord('tag_time',tag_time,idUserDiscord)

                        if avatar_time_url != dadosUserDiscord['data']['avatar_time_url']:
                            atualiiarDadosUserDiscord('avatar_time_url',avatar_time_url,idUserDiscord)

                        if funcao_no_time != dadosUserDiscord['data']['funcao_no_time']:
                            atualiiarDadosUserDiscord('funcao_no_time',funcao_no_time,idUserDiscord)

                        if posicao_no_time != dadosUserDiscord['data']['posicao_no_time']:
                            atualiiarDadosUserDiscord('posicao_no_time',posicao_no_time,idUserDiscord)
                else:
                    formatarNomeTime = []
                    dadosTimeAll = GetTimes()
                    for time in dadosTimeAll:
                        formatarNomeTime.append(time.lower().strip())

                    for roles in interaction.user.roles:
                        if roles.name == '@everyone':
                            pass
                        else:
                            cargoNome = roles.name.split('┇')[1].strip().lower()
                            if cargoNome in formatarNomeTime:
                                await interaction.user.remove_roles(roles)
                                break

                    embed = discord.Embed(
                        title=f"`👤` {username} • Perfil Competitivo",
                        description=(
                            "`🏆` Perfil competitivo MIXCAMP\n"
                            "`🎮` Jogador competitivo de CS2"
                        ),
                        color=discord.Color.from_str(cores_perfil)
                    )

                    # =========================================================
                    # AVATAR
                    # =========================================================

                    embed.set_thumbnail(url=avatar_url)

                    # =========================================================
                    # DADOS GERAIS
                    # =========================================================

                    embed.add_field(
                        name="`🆔` Informações Gerais",
                        value=(
                            f"`🆔` ID: `{idMixcamp}`\n"
                            f"`👤` Username: `{username}`\n"
                            f"`📧` Email: `{email}`\n"
                            f"`🛡️` Gerência: `{gerencia}`\n"
                            f"`💎` Organizador: `{organizador}`"
                        ),
                        inline=False
                    )

                    # =========================================================
                    # COMPETITIVO
                    # =========================================================

                    embed.add_field(
                        name="`🎮` Competitivo",
                        value=(
                            f"`🚂` SteamID: `{steamid}`\n"
                            f"`🎯` FACEIT ID: `{faceitid}`"
                        ),
                        inline=False
                    )

                    # =========================================================
                    # ESTATISTICAS
                    # =========================================================

                    embed.add_field(
                        name="`📊` Estatísticas",
                        value=(
                            f"`🏅` Medalhas: `{total_medalhas}`\n"
                            f"`🎬` Destaques: `{total_destaques}`"
                        ),
                        inline=True
                    )

                    # =========================================================
                    # POSIÇÕES
                    # =========================================================

                    embed.add_field(
                        name="`🎯` Roles",
                        value=f"```{posicoes}```",
                        inline=True
                    )

                    # =========================================================
                    # REDES SOCIAIS
                    # =========================================================

                    redes = []

                    if discord_url:
                        redes.append(f"[Discord]({discord_url})")

                    if instagram_url:
                        redes.append(f"[Instagram]({instagram_url})")

                    if youtube_url:
                        redes.append(f"[YouTube]({youtube_url})")

                    if twitch_url:
                        redes.append(f"[Twitch]({twitch_url})")

                    if faceit_url:
                        redes.append(f"[FACEIT]({faceit_url})")

                    if gamesclub_url:
                        redes.append(f"[GamersClub]({gamesclub_url})")

                    if steam_url:
                        redes.append(f"[Steam]({steam_url})")

                    if twitter_url:
                        redes.append(f"[Twitter]({twitter_url})")

                    if tiktok_url:
                        redes.append(f"[TikTok]({tiktok_url})")

                    if kick_url:
                        redes.append(f"[Kick]({kick_url})")

                    if allstar_url:
                        redes.append(f"[AllStar]({allstar_url})")

                    if len(redes) > 0:

                        embed.add_field(
                            name="`🌐` Redes Sociais",
                            value=" • ".join(redes),
                            inline=False
                        )

                    # =========================================================
                    # CFG
                    # =========================================================

                    if link_cfg:

                        embed.add_field(
                            name="`⚙️` CFG CS2",
                            value=f"[📥 Download CFG]({link_cfg})",
                            inline=False
                        )

                    # =========================================================
                    # FOOTER
                    # =========================================================

                    embed.set_footer(
                        text="MIXCAMP • Perfil Competitivo"
                    )

                    await interaction.followup.send(
                        embed=embed,
                        ephemeral=True
                    )

                    novoApelido = ''
                    await interaction.user.edit(nick=f"")

                    if steamid is not None or faceitid is not None:
                        novoApelido = '✔'+novoApelido

                    

                    if idMixcamp == lider_id:
                        novoApelido = novoApelido + '👑'

                    if gerencia == 'admin':
                        novoApelido = novoApelido +'⚙️'
                        await adicionar_cargo(interaction.user, interaction.guild, STAFF)
                    elif gerencia == 'moderador':
                        novoApelido = novoApelido +'🛡️'
                        await adicionar_cargo(interaction.user, interaction.guild, MODERADOR)
                    elif gerencia == 'streamer':
                        novoApelido = novoApelido + '🎥'
                        await adicionar_cargo(interaction.user, interaction.guild, STREAMER)
                    if organizador == 'premium':
                        novoApelido = novoApelido + '🏆'

                    elif organizador == 'simples':
                        novoApelido = novoApelido + '🥇'


                    await interaction.user.edit(nick=f"{novoApelido}┇{username}")


                    
                    atualiiarDadosUserDiscord('time_id',None,idUserDiscord)

                    
                    atualiiarDadosUserDiscord('lider_id',None,idUserDiscord)

                    
                    atualiiarDadosUserDiscord('nome_time',None,idUserDiscord)

                
                    atualiiarDadosUserDiscord('tag_time',None,idUserDiscord)

                
                    atualiiarDadosUserDiscord('avatar_time_url',None,idUserDiscord)

                
                    atualiiarDadosUserDiscord('funcao_no_time',None,idUserDiscord)

                
                    atualiiarDadosUserDiscord('posicao_no_time',None,idUserDiscord)



            else:
                formatarNomeTime = []
                dadosTimeAll = GetTimes()
                for time in dadosTimeAll:
                    formatarNomeTime.append(time.lower().strip())

                for roles in interaction.user.roles:
                    if roles.name == '@everyone':
                        pass
                    else:
                        cargoNome = roles.name.split('┇')[1].strip().lower()
                        if cargoNome in formatarNomeTime:
                            await interaction.user.remove_roles(roles)
                            break

                
                atualiiarDadosUserDiscord('time_id',None,idUserDiscord)

            
                atualiiarDadosUserDiscord('lider_id',None,idUserDiscord)

            
                atualiiarDadosUserDiscord('nome_time',None,idUserDiscord)

            
                atualiiarDadosUserDiscord('tag_time',None,idUserDiscord)

            
                atualiiarDadosUserDiscord('avatar_time_url',None,idUserDiscord)

            
                atualiiarDadosUserDiscord('funcao_no_time',None,idUserDiscord)

            
                atualiiarDadosUserDiscord('posicao_no_time',None,idUserDiscord)

                embed = discord.Embed(
                    title=f"`👤` {username} • Perfil Competitivo",
                    description=(
                        "`🏆` Perfil competitivo MIXCAMP\n"
                        "`🎮` Jogador competitivo de CS2"
                    ),
                    color=discord.Color.from_str(cores_perfil)
                )

                # =========================================================
                # AVATAR
                # =========================================================

                embed.set_thumbnail(url=avatar_url)

                # =========================================================
                # DADOS GERAIS
                # =========================================================

                embed.add_field(
                    name="`🆔` Informações Gerais",
                    value=(
                        f"`🆔` ID: `{idMixcamp}`\n"
                        f"`👤` Username: `{username}`\n"
                        f"`📧` Email: `{email}`\n"
                        f"`🛡️` Gerência: `{gerencia}`\n"
                        f"`💎` Organizador: `{organizador}`"
                    ),
                    inline=False
                )

                # =========================================================
                # COMPETITIVO
                # =========================================================

                embed.add_field(
                    name="`🎮` Competitivo",
                    value=(
                        f"`🚂` SteamID: `{steamid}`\n"
                        f"`🎯` FACEIT ID: `{faceitid}`"
                    ),
                    inline=False
                )

                # =========================================================
                # ESTATISTICAS
                # =========================================================

                embed.add_field(
                    name="📊 Estatísticas",
                    value=(
                        f"`🏅` Medalhas: `{total_medalhas}`\n"
                        f"`🎬` Destaques: `{total_destaques}`"
                    ),
                    inline=True
                )

                # =========================================================
                # POSIÇÕES
                # =========================================================

                embed.add_field(
                    name="`🎯` Roles",
                    value=f"```{posicoes}```",
                    inline=True
                )

                # =========================================================
                # REDES SOCIAIS
                # =========================================================

                redes = []

                if discord_url:
                    redes.append(f"[Discord]({discord_url})")

                if instagram_url:
                    redes.append(f"[Instagram]({instagram_url})")

                if youtube_url:
                    redes.append(f"[YouTube]({youtube_url})")

                if twitch_url:
                    redes.append(f"[Twitch]({twitch_url})")

                if faceit_url:
                    redes.append(f"[FACEIT]({faceit_url})")

                if gamesclub_url:
                    redes.append(f"[GamersClub]({gamesclub_url})")

                if steam_url:
                    redes.append(f"[Steam]({steam_url})")

                if twitter_url:
                    redes.append(f"[Twitter]({twitter_url})")

                if tiktok_url:
                    redes.append(f"[TikTok]({tiktok_url})")

                if kick_url:
                    redes.append(f"[Kick]({kick_url})")

                if allstar_url:
                    redes.append(f"[AllStar]({allstar_url})")

                if len(redes) > 0:

                    embed.add_field(
                        name="`🌐` Redes Sociais",
                        value=" • ".join(redes),
                        inline=False
                    )

                # =========================================================
                # CFG
                # =========================================================

                if link_cfg:

                    embed.add_field(
                        name="`⚙️` CFG CS2",
                        value=f"[📥 Download CFG]({link_cfg})",
                        inline=False
                    )

                # =========================================================
                # FOOTER
                # =========================================================

                embed.set_footer(
                    text="MIXCAMP • Perfil Competitivo"
                )

                await interaction.followup.send(
                    embed=embed,
                    ephemeral=True
                )

                novoApelido = ''
                await interaction.user.edit(nick=f"")

                if steamid is not None or faceitid is not None:
                    novoApelido = '✔'+novoApelido

                if gerencia == 'admin':
                    novoApelido = novoApelido +'⚙️'
                    await adicionar_cargo(interaction.user, interaction.guild, STAFF)
                elif gerencia == 'moderador':
                    novoApelido = novoApelido +'🛡️'
                    await adicionar_cargo(interaction.user, interaction.guild, MODERADOR)
                elif gerencia == 'streamer':
                    novoApelido = novoApelido + '🎥'
                    await adicionar_cargo(interaction.user, interaction.guild, STREAMER)
                if organizador == 'premium':
                    novoApelido = novoApelido + '🏆'

                elif organizador == 'simples':
                    novoApelido = novoApelido + '🥇'


                await interaction.user.edit(nick=f"{novoApelido}┇{username}")


                

                

                
        else:
            await interaction.followup.send(
                "❌ Erro ao buscar dados do usuário no MixCamp.",
                ephemeral=True
            )
            return
    else:
        await interaction.followup.send(
            "❌ Você não está registrado no sistema de perfil.",
            ephemeral=True
        )
        return


async def criarCanaisTimes(interaction: discord.Interaction,listaDeTimesDoCampeonato: list):

    guild = interaction.guild

    if not guild:
        return await interaction.response.send_message("Erro: servidor não encontrado.", ephemeral=True)

    for time in listaDeTimesDoCampeonato:
        categoria = await guild.create_category(f"🎮 {time}")
        await guild.create_text_channel("chat-geral", category=categoria)
        await guild.create_voice_channel("Sala 1", category=categoria)

    await interaction.response.send_message("Categorias e canais criados com sucesso!")

# =========================================================
# CONFIG CAMPEONATOS PARA CRIAÇÃO DE SALAS DE TIMES AUTOMÁTICAS
# =========================================================

campeonatos = [
    "mx_league",
]

seasons_campeonatos = {
    "mx_league": []
}

# =========================================================

# =========================================================
# SELECT DE SEASON
# =========================================================

class SelectSeasonCampeonato(discord.ui.Select):

    def __init__(self, campeonato):

        seasons = seasons_campeonatos.get(campeonato, [])

        options = [
            discord.SelectOption(
                label=season,
                value=season
            )
            for season in seasons
        ]

        super().__init__(
            placeholder="Escolha a season",
            min_values=1,
            max_values=1,
            options=options
        )

        self.campeonato = campeonato

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        season_escolhida = self.values[0]
        season_escolhida = season_escolhida.split(' ')[1]

        listaDeTimesDoCampeonato = getTimesAllCampeonatos(season_escolhida)['data']
        await criarCanaisTimes(interaction,listaDeTimesDoCampeonato)

        await interaction.followup.send(
            f"🏆 Campeonato: {self.campeonato}\n📅 Season: {season_escolhida}",
            ephemeral=True
        )
        
# =========================================================
# VIEW DE SEASON
# =========================================================

class ViewSeason(discord.ui.View):

    def __init__(self, campeonato):
        super().__init__(timeout=None)

        self.add_item(SelectSeasonCampeonato(campeonato))

# =========================================================
# SELECT DE CAMPEONATO
# =========================================================

class SelectCampeonato(discord.ui.Select):

    def __init__(self):

        options = [
            discord.SelectOption(
                label=camp,
                value=camp
            )
            for camp in campeonatos
        ]

        super().__init__(
            placeholder="Escolha o campeonato",
            min_values=1,
            max_values=1,
            options=options
        )

    async def callback(self, interaction: discord.Interaction):

        # VF

        verificaPermissao = False


        for nameroles in interaction.guild.roles:
            if nameroles.name == '@everyone':
                pass
            else:
                cargoNome = nameroles.name.split('┇')[1].strip().lower()
                print(cargoNome)

                if cargoNome == 'owner':
                    verificaPermissao = True

        

        if verificaPermissao == False:
            
            await interaction.response.send_message(
                "❌ Você não possui permissão para selecionar um campeonato.",
                ephemeral=True
            )
            return
        else:
            


            campeonato_escolhido = self.values[0]

            listaDaSeasons = getSeasons()

            if listaDaSeasons['status']:
                for season in listaDaSeasons['data']['seasons']:
                    seasons_campeonatos["mx_league"].append(f"Season {season}")



            await interaction.response.send_message(
                f"🏆 Campeonato selecionado: {campeonato_escolhido}",
                view=ViewSeason(campeonato_escolhido),
                ephemeral=True
            )

# =========================================================
# VIEW CAMPEONATO
# =========================================================

class ViewCampeonato(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

        self.add_item(SelectCampeonato())

# =========================================================
# BOTÃO PRINCIPAL
# =========================================================

class PainelCampeonato(discord.ui.View):

    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Selecionar Campeonato",
        style=discord.ButtonStyle.primary,
        emoji="🏆"
    )
    async def selecionar(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        await interaction.response.send_message(
            "Escolha um campeonato:",
            view=ViewCampeonato(),
            ephemeral=True
        )

# =========================================================
# =========================================================

class PainelPerfilView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Atualizar Perfil",
        style=discord.ButtonStyle.primary,
        emoji="🔄",
        custom_id="atualizar_perfil_button"
    )
    async def atualizar_perfil(self,interaction: discord.Interaction,button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)

        await MostrarOuAtualizarPerfil(interaction)

       
# =========================================================
# SELECT MENU DE SEASONS
# =========================================================

class SelectSeason(discord.ui.Select):
    def __init__(
        self,
        seasons,
        primeiro_time,
        segundo_time,
        data_jogo,
        horario
    ):

        options = []

        # =====================================================
        # VOCÊ VAI TROCAR ESSA LÓGICA PELA API
        # =====================================================

        for season in seasons:

            options.append(
                discord.SelectOption(
                    label=season,
                    value=season.lower().replace(" ", "_")
                )
            )

        super().__init__(
            placeholder="Selecione a season",
            min_values=1,
            max_values=1,
            options=options
        )

        self.primeiro_time = primeiro_time
        self.segundo_time = segundo_time
        self.data_jogo = data_jogo
        self.horario = horario


    async def callback(self, interaction: discord.Interaction):


        season_escolhida = self.values[0]
        season_escolhida = season_escolhida.split('_')[1]
        dadosUser = getDadosUserDiscord(interaction.user.id)
        if dadosUser['status']:
            idMixcamp = dadosUser['data'][2]

        dados = AmarzenarAgendamento(idMixcamp,self.primeiro_time,self.segundo_time,self.data_jogo,self.horario,season_escolhida,'mx_league')

        if dados['status']:

            await interaction.response.send_message(
                f"""
                `🏆` **Campeonato: MX LEAGUE - {season_escolhida}**
                **==================================================**
                `🏆` **{self.primeiro_time}** `🆚` **{self.segundo_time}** `🏆`
                `📅` **Data:** **{self.data_jogo}**
                `⏰` **Horário:** **{self.horario}**
                ---------------------------------
                `✅` **Agendamento concluído com sucesso verifique com comando /veragendamentos!**
            """,
            ephemeral=True
            )
        else:
            print(dados['mensagem'])
            await interaction.response.send_message(
                f"""`❌` **Erro ao agendar jogo:**
            """,
            ephemeral=True
            )

# =========================================================
# VIEW DO SELECT
# =========================================================

class SeasonView(discord.ui.View):
    def __init__(
        self,
        seasons,
        primeiro_time,
        segundo_time,
        data_jogo,
        horario
    ):

        super().__init__(timeout=120)

        self.add_item(
            SelectSeason(
                seasons,
                primeiro_time,
                segundo_time,
                data_jogo,
                horario
            )
        )

# =========================================================
# BOTÃO
# =========================================================

class PainelAgendamento(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="📆Agendar Jogo",
        style=discord.ButtonStyle.primary,
        custom_id="agendar_jogo"
    )
    async def agendar_jogo(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        await interaction.response.send_modal(
            ModalAgendarJogo()
        )

# =========================================================
# MODAL
# =========================================================

class ModalAgendarJogo(discord.ui.Modal, title="Agendar Jogo"):

    primeiro_time_nome = discord.ui.TextInput(
        label="Nome do Time 1",
        placeholder="Ex: Team Furia",
        required=True,
        max_length=100
    )

    segundo_time_nome = discord.ui.TextInput(
        label="Nome do Time 2",
        placeholder="Ex: Team Pain",
        required=True,
        max_length=100
    )

    data_do_jogo = discord.ui.TextInput(
        label="Data do jogo",
        placeholder="Ex: 01/05/2026",
        required=True,
        max_length=20
    )

    horario_inicio = discord.ui.TextInput(
        label="Horário",
        placeholder="Ex: 20:00",
        required=True,
        max_length=10
    )

    async def on_submit(self, interaction: discord.Interaction):

        primeiro_time = self.primeiro_time_nome.value.upper()
        segundo_time = self.segundo_time_nome.value.upper()
        data_jogo = self.data_do_jogo.value
        horario = self.horario_inicio.value

        if len(data_jogo)  < 8:
            return await interaction.response.send_message(
                "❌ Data inválida. Envie uma data válida.",
                ephemeral=True
            )
        
        if len(horario) < 5:
            return await interaction.response.send_message(
                "❌ Horário inválido. Envie um horário válido.",
                ephemeral=True
            )

        
            

        # =====================================================
        # LISTA TEMPORÁRIA
        # =====================================================

        lista_seasons = []

        """
        ========================================================
        AQUI VOCÊ VAI BUSCAR SUA API
        ========================================================
        """

        dadosSeasons = getSeasons()
        if dadosSeasons['status']:
            for season in dadosSeasons['data']['seasons']:
                lista_seasons.append(f"Season {season}")

        

        dadosUser = getDadosUserDiscord(interaction.user.id)
        if dadosUser['status']:
            idMixcamp = dadosUser['data'][2]
            liderTime = dadosUser['data'][10]
            funcaoNoTime = dadosUser['data'][14]
        else:
            await interaction.response.send_message(
                "❌ Erro ao buscar dados do usuário no MixCamp.",
                ephemeral=True
            )
            return

        if idMixcamp != liderTime and funcaoNoTime != 'coach':
            await interaction.response.send_message(
                "❌ Você não possui permissão para agendar jogo, apenas líder ou coach do time.",
                ephemeral=True
            )
            return


        await interaction.response.send_message(
            content=(
                f"`✅` **Agora selecione a Season do Campeonato abaixo:**"
            ),
            view=SeasonView(
                lista_seasons,
                primeiro_time,
                segundo_time,
                data_jogo,
                horario
            ),
            ephemeral=True
        )
# =======================================================
# ================= MODAL INDENTIFICACAO ================
# =======================================================
class LinkModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="🔗 Enviar Link do Perfil")

        self.link = discord.ui.TextInput(
            label="Cole o link aqui",
            placeholder="https://mikedcf.github.io/mixcamp/frontend/html/perfil.html?id=",
            required=True,
            max_length=500
        )

        self.add_item(self.link)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)

        url = self.link.value.strip()

        # 🔒 validação simples
        if not url.startswith("http"):
            return await interaction.followup.send(
                "❌ Link inválido. Envie uma URL válida.",
                ephemeral=True
            )

        verificarUserExistente =getDadosUserDiscord(interaction.user.id)

        if verificarUserExistente['status']:
            await interaction.followup.send(
                "❌ Você já está registrado no MixCamp.",
                ephemeral=True
            )
            return




        dados = Verificar_extrairID(url)
        veryTime = True
        novoApelido = ''

        if dados['status']:
            dadosPlayer = DadosplayerID(dados['id'])

            if dadosPlayer['status']:
            

                # dados do usuario
                UserMixcampID = dadosPlayer['userDados']['userDados'][0]['id']
                usernameMixcamp = dadosPlayer['userDados']['userDados'][0]['username']
                steamID = dadosPlayer['userDados']['userDados'][0]['steamid']
                faceitID = dadosPlayer['userDados']['userDados'][0]['faceitid']
                avatarURL = dadosPlayer['userDados']['userDados'][0]['avatar_url']
                gerencia = dadosPlayer['userDados']['userDados'][0]['gerencia']
                organizador = dadosPlayer['userDados']['userDados'][0]['organizador']
                timeID = dadosPlayer['userDados']['userDados'][0]['time_id']

                if organizador == None:
                    organizador = 'null'
                    
                if gerencia == 'streammer':
                    gerencia = 'streamer'

                

                if faceitID == None or faceitID == '' or faceitID == 'null' and steamID == None or steamID == '' or steamID == 'null':
                    pass
                else:
                    novoApelido = f'✔'

                # # dados time do user

                if dadosPlayer['userDados']['userDados'][0]['time_id'] == None:
                    veryTime = False

                if veryTime:
                    await AtualizarCargoTimes(interaction.guild)
                    
                    
                    liderTimeID = dadosPlayer['userDados']['userDados'][0]['lider_id']
                    nomeTime = dadosPlayer['userDados']['userDados'][0]['nome']
                    tagTime = dadosPlayer['userDados']['userDados'][0]['tag']
                    avatarTimeURL = dadosPlayer['userDados']['userDados'][0]['avatar_time_url']
                    funcaoDoUserNoTime = dadosPlayer['userDados']['userDados'][0]['funcao']
                    posicaoDoUserNoTime = dadosPlayer['userDados']['userDados'][0]['posicao']


                    
                    if gerencia == 'admin':
                        novoApelido = novoApelido +'⚙️'
                        await adicionar_cargo(interaction.user, interaction.guild, STAFF)

                    elif gerencia == 'moderador':
                        novoApelido = novoApelido +'🛡️'
                        await adicionar_cargo(interaction.user, interaction.guild, MODERADOR)

                    elif gerencia == 'Coach':
                        novoApelido = novoApelido + '🎧'

                    elif gerencia == 'streamer':
                        novoApelido = novoApelido + '🎥'
                        await adicionar_cargo(interaction.user, interaction.guild, STREAMER)

                    if organizador == 'premium':
                        novoApelido = novoApelido + '🏆'

                    elif organizador == 'simples':
                        novoApelido = novoApelido + '🥇'

                    if UserMixcampID == liderTimeID:
                        novoApelido = novoApelido + '👑'



                    

                    

                    for nameroles in interaction.guild.roles:
                        if nameroles.name == '@everyone':
                            pass
                        else:
                            cargoNome = nameroles.name.split('┇')[1].strip().lower()

                            if cargoNome == nomeTime.lower():
                                await interaction.user.edit(nick=f"")
                                await interaction.user.add_roles(nameroles)
                                novoApelido = novoApelido + f'｢{tagTime}｣┇ {usernameMixcamp}'
                                await interaction.user.edit(nick=f"{novoApelido}")
                                break

                    await adicionar_cargo(interaction.user, interaction.guild, VERIFICADO)


                    ArmazenarDadosUserDiscord(interaction.user.id,UserMixcampID,usernameMixcamp,interaction.user.name,steamID,faceitID,avatarURL,gerencia,organizador,liderTimeID,nomeTime,tagTime,avatarTimeURL,funcaoDoUserNoTime,posicaoDoUserNoTime,timeID)

                    

                    webhook_url = getDadosSistema('c-logs')['data']['webhook_url']

                    embed = {
                        "title": "✅ Dados armazenados com sucesso!",
                        "color": 0x00BFFF,  # Azul ciano
                        "thumbnail": {
                            "url": avatarURL
                        },
                        "fields": [
                            {
                                "name": "👤 Discord",
                                "value": f"{interaction.user.name}",
                                "inline": True
                            },
                            {
                                "name": "🆔 Discord ID",
                                "value": f"{interaction.user.id}",
                                "inline": True
                            },
                            {
                                "name": "🆔 MixCamp ID",
                                "value": f"{UserMixcampID}",
                                "inline": True
                            },
                            {
                                "name": "🎮 Username MixCamp",
                                "value": f"{usernameMixcamp}",
                                "inline": True
                            },
                            {
                                "name": "🚂 Steam ID",
                                "value": f"{steamID}",
                                "inline": True
                            },
                            {
                                "name": "🎯 Faceit ID",
                                "value": f"{faceitID}",
                                "inline": True
                            },
                            {
                                "name": "👥 Nome do Time",
                                "value": f"{nomeTime}",
                                "inline": True
                            },
                            {
                                "name": "🏷️ Tag do Time",
                                "value": f"{tagTime}",
                                "inline": True
                            },
                            {
                                "name": "👑 Líder ID",
                                "value": f"{liderTimeID}",
                                "inline": True
                            },
                            {
                                "name": "🖼️ Avatar do Time",
                                "value": f"[Clique Aqui]({avatarTimeURL})",
                                "inline": False
                            },
                            {
                                "name": "🎖️ Função",
                                "value": f"{funcaoDoUserNoTime}",
                                "inline": True
                            },
                            {
                                "name": "📍 Posição",
                                "value": f"{posicaoDoUserNoTime}",
                                "inline": True
                            }
                        ],
                        "footer": {
                            "text": "MIXCAMP • Sistema de Registro"
                        }
                    }

                    data = {
                        "embeds": [embed]
                    }

                    requests.post(webhook_url, json=data)

                    msg = f"usuario @{interaction.user.name} do discord foi associado a sua conta no MixCamp!"


                    enviarNotificacaoSiteMixcamp(UserMixcampID,msg)

                
                    await interaction.followup.send('✅**Você foi registrado no cargo do seu time.**', ephemeral=True)
                    await interaction.followup.send(f'✅**Seu apelido foi alterado para {novoApelido} **', ephemeral=True)
                    

                else:
                    if gerencia == 'admin':
                        novoApelido = novoApelido +'👷'+ f'┇ {usernameMixcamp}'
                        await adicionar_cargo(interaction.user, interaction.guild, STAFF)
                    elif gerencia == 'moderador':
                        novoApelido = novoApelido +'🛡️'+ f'┇ {usernameMixcamp}'
                        await adicionar_cargo(interaction.user, interaction.guild, MODERADOR)
                    elif gerencia == 'streamer':
                        novoApelido = novoApelido + '🎥'+ f'┇ {usernameMixcamp}'
                        await adicionar_cargo(interaction.user, interaction.guild, STREAMER)
                    if organizador == 'premium':
                        novoApelido = novoApelido + '🏆'+ f'┇ {usernameMixcamp}'

                    elif organizador == 'simples':
                        novoApelido = novoApelido + '🥇'+ f'┇ {usernameMixcamp}'

                    else:
                        novoApelido = novoApelido + f'┇ {usernameMixcamp}'

                    await interaction.user.edit(nick=f"{novoApelido}")
                    await adicionar_cargo(interaction.user, interaction.guild, VERIFICADO)

                    ArmazenarDadosUserDiscord(interaction.user.id,UserMixcampID,usernameMixcamp,interaction.user.name,steamID,faceitID,avatarURL,gerencia,organizador)

                    webhook_url = getDadosSistema('c-logs')['data']['webhook_url']

                    embed = {
                        "title": "✅ Dados armazenados com sucesso!",
                        "color": 0x00BFFF,  # Azul ciano
                        "thumbnail": {
                            "url": avatarURL
                        },
                        "fields": [
                            {
                                "name": "👤 Discord",
                                "value": f"{interaction.user.name}",
                                "inline": True
                            },
                            {
                                "name": "🆔 Discord ID",
                                "value": f"{interaction.user.id}",
                                "inline": True
                            },
                            {
                                "name": "🆔 MixCamp ID",
                                "value": f"{UserMixcampID}",
                                "inline": True
                            },
                            {
                                "name": "🎮 Username MixCamp",
                                "value": f"{usernameMixcamp}",
                                "inline": True
                            },
                            {
                                "name": "🚂 Steam ID",
                                "value": f"{steamID}",
                                "inline": True
                            },
                            {
                                "name": "🎯 Faceit ID",
                                "value": f"{faceitID}",
                                "inline": True
                            },
                            {
                                "name": "🖼️ Avatar URL",
                                "value": f"[Clique Aqui]({avatarURL})",
                                "inline": False
                            }
                        ],
                        "footer": {
                            "text": "MIXCAMP • Sistema de Registro"
                        }
                    }

                    data = {
                        "embeds": [embed]
                    }


                    requests.post(webhook_url, json=data)

                    canalPerfilId = getDadosSistema('c-perfil')['data']['id_tipo']


                    msg = f"usuario @{interaction.user.name} do discord foi associado a sua conta no MixCamp!"


                    enviarNotificacaoSiteMixcamp(UserMixcampID,msg)
                    


                    await interaction.followup.send('✅**Você foi registrado no cargo do seu time.**', ephemeral=True)
                    await interaction.followup.send(f'✅**Seu apelido foi alterado para {novoApelido} - verifique o canal <#{canalPerfilId}> **', ephemeral=True) 
            else:
                await interaction.followup.send(
                    "❌ Erro ao buscar dados do usuário no MixCamp.",
                    ephemeral=True
                )
                return

        else:
            await interaction.followup.send(
                "❌ Link inválido. Envie uma URL válida.",
                ephemeral=True
            )
        
class LinkButton(discord.ui.Button):
    def __init__(self):
        super().__init__(
            label="Enviar link do Perfil",
            style=discord.ButtonStyle.primary,
            emoji="🔗",
            custom_id="enviar_link_btn"  # 🔥 OBRIGATÓRIO
        )

    async def callback(self, interaction: discord.Interaction):
        # interaction.response.defer(ephemeral=True)
        await interaction.response.send_modal(LinkModal())

class LinkView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(LinkButton())

# =======================================================
# ================= SISTEMA DE TICKETS ==================
# =======================================================
class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Abrir Ticket",
        emoji="🎫",
        style=discord.ButtonStyle.primary,
        custom_id="ticket_open"
    )
    async def abrir(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(
            f"{interaction.user.mention}**Escolha o tipo de ticket `⬇️`:**",
            view=SelectTicketView(),
            ephemeral=True
        )
class SelectTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)
        self.add_item(SelectTicket())
class TicketModal(discord.ui.Modal, title="Abrir Ticket"):

    def __init__(self, tipo):
        super().__init__()
        self.tipo = tipo

        self.descricao = discord.ui.TextInput(
            label="Descreva seu problema",
            style=discord.TextStyle.paragraph,
            placeholder="Explique detalhadamente...",
            required=True,
            max_length=500
        )

        self.add_item(self.descricao)

    async def on_submit(self, interaction: discord.Interaction):
        await criar_ticket(interaction, self.tipo, self.descricao.value)
class SelectTicket(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Bug no site", value="bug", emoji="📑"),
            discord.SelectOption(label="Reportar player", value="report", emoji="👮"),
            discord.SelectOption(label="Problemas técnicos", value="tecnico", emoji="⚙️"),
            discord.SelectOption(label="Sugestões", value="sugestao", emoji="📝"),
            discord.SelectOption(label="Dúvidas", value="duvida", emoji="💬"),
        ]

        super().__init__(
            placeholder="Selecione o tipo...",
            options=options,
            custom_id="ticket_select"
        )

    async def callback(self, interaction: discord.Interaction):
        tipo = self.values[0]  # pode usar direto assim também

        await interaction.response.send_modal(TicketModal(tipo))


class CloseTicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(
        label="Fechar Ticket",
        emoji="🔒",
        style=discord.ButtonStyle.danger,
        custom_id="close_ticket"
    )
    async def fechar(self, interaction: discord.Interaction, button: discord.ui.Button):

        await interaction.response.defer(ephemeral=True)
        # nome do canal
        cargosLiders = False
        
        nomeCanal = interaction.channel.name
        nomeCanal = nomeCanal.split('┇')
        nomeCanal = nomeCanal[1].capitalize().strip()
        numberTicket = nomeCanal.split('-')[1]
        UserID = getDadosTicket('number_ticket',numberTicket)['data'][1]
        


        cargos = interaction.user.roles
        for cargo in cargos:
            if cargo.id == CEO or cargo.id == STAFF:
                cargosLiders = True
                break

        if cargosLiders:
            for nameroles in interaction.guild.roles:
                if nameroles.name == '@everyone':
                    pass
                else:
                    cargoNome = nameroles.name.split('┇')[1].strip()
                    if cargoNome == nomeCanal:

                        await interaction.followup.send(
                            "🔒** Ticket vai ser encerrado em 5 segundos!**",
                            ephemeral=True
                        )

                        await asyncio.sleep(5)
                        webhook_url = getDadosSistema('c-solicitacoes-tickets')['data'][4]
                        AtualizarDadosTicket(numberTicket,False)

                        async with aiohttp.ClientSession() as session:
                            await session.post(webhook_url, json={
                                "content": f"<@&{CEO}> <@&{STAFF}>",
                                "embeds": [
                                    {
                                        "title": "🔒 Ticket Fechado",
                                        "description": "O ticket foi encerrado.",
                                        "color": 15158332,

                                        "thumbnail": {
                                            "url": interaction.user.display_avatar.url
                                        },

                                        "fields": [
                                            {
                                                "name": "📂 Canal",
                                                "value": f"`🎫⡇Ticket-{numberTicket}`",
                                                "inline": True
                                            },
                                            {
                                                "name": "👤 Responsável",
                                                "value": interaction.user.mention,
                                                "inline": True
                                            }
                                        ],

                                        "footer": {
                                            "text": "MIXCAMP • Logs"
                                        },

                                    }
                                ]
                            })

                        

                        user = await bot.fetch_user(UserID)
                        await user.send(f"""**🔒 Olá! Seu `🎫⡇Ticket-{numberTicket}` foi fechado pelo {interaction.user.mention}.\n**""")
                        
                        cargo = interaction.guild.get_role(nameroles.id)

                        if cargo:
                            await cargo.delete()
                        await interaction.channel.delete()
                        break
        
        else:

            for nameroles in interaction.guild.roles:
                if nameroles.name == '@everyone':
                    pass
                else:
                    cargoNome = nameroles.name.split('┇')[1].strip()
                    if cargoNome == nomeCanal:

                        await interaction.followup.send(
                            "🔒** Ticket vai ser encerrado em 5 segundos!**",
                            ephemeral=True
                        )

                        await asyncio.sleep(5)
                        webhook_url = getDadosSistema('c-solicitacoes-tickets')['data'][4]
                        AtualizarDadosTicket(numberTicket,False)

                        async with aiohttp.ClientSession() as session:
                            await session.post(webhook_url, json={
                                "content": f"<@&{CEO}> <@&{STAFF}>",
                                "embeds": [
                                    {
                                        "title": "🔒 Ticket Fechado",
                                        "description": "O ticket foi encerrado.",
                                        "color": 15158332,

                                        "thumbnail": {
                                            "url": interaction.user.display_avatar.url
                                        },

                                        "fields": [
                                            {
                                                "name": "📂 Canal",
                                                "value": f"`🎫⡇Ticket-{numberTicket}`",
                                                "inline": True
                                            },
                                            {
                                                "name": "👤 Responsável",
                                                "value": interaction.user.mention,
                                                "inline": True
                                            }
                                        ],

                                        "footer": {
                                            "text": "MIXCAMP • Logs"
                                        },
                                    }
                                ]
                            })

                        cargo = interaction.guild.get_role(nameroles.id)
                        if cargo:
                            await cargo.delete()

                        await interaction.channel.delete()
                        break
        

async def criar_ticket(interaction, tipo, descricao):

    await interaction.response.defer(ephemeral=True)


    if tipo in [ 'bug','report','tecnico','duvida']:
        number_ticket = 0
        if getNumeroTicket()['status']:
            if getNumeroTicket()['data'] is None:
                number_ticket = 1
            else:
                number_ticket = getNumeroTicket()['data'] + 1

        cargoTicket = await interaction.guild.create_role(
            name=f"'🎟️┇Ticket-{number_ticket}",
            colour=discord.Colour.orange(),
            hoist=False,
            mentionable=True,
            permissions=discord.Permissions(administrator=False)
        )

        await interaction.user.add_roles(cargoTicket)


        guild = interaction.guild
        cargo_ceo = guild.get_role(CEO)
        cargo_staff = guild.get_role(STAFF)


        categoria = guild.get_channel(CATEGORIATICKETID)

        if not categoria:
            await interaction.response.send_message(
                "Categoria não encontrada.",
                ephemeral=True
            )
            return
        

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False), 

            cargo_ceo: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True
            ),

            cargo_staff: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True
            ),

            cargoTicket: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True
            )
        }


        

        canalTicket = await interaction.guild.create_text_channel(
            name=f"🎟️┇Ticket-{number_ticket}",
            category=categoria,
            overwrites=overwrites
        )

        userid = interaction.user.id
        username = interaction.user.name
        problema = descricao
        cargo_id = cargoTicket.id
        canal_id = canalTicket.id

        armazenarDadosTicket(userid,username,tipo,problema,number_ticket,cargo_id,canal_id)

        


        embed = discord.Embed(
            title=f"`🎫` Ticket - {number_ticket} Aberto!",
            description=(
                f"**Usuário:** {interaction.user.mention}\n"
                f"**Tipo:** {tipo}\n\n"
                f"**Mensagem:**\n{descricao}"
            ),
            color=discord.Color.red()
        )

        webhook_url = getDadosSistema('c-solicitacoes-tickets')['data'][4]

        requests.post(webhook_url, json={
            "content": f"<@&{CEO}> <@&{STAFF}>\n **Ticket Aberto:** {canalTicket.mention}",
            "embeds": [embed.to_dict()]
        })

        embed = discord.Embed(
            title=f"`🎫` Ticket - {number_ticket} Aberto!",
            description=(
                f"**{interaction.user.mention} Entrei em contato com o suporte, agora e so aguardar a resposta!**\n"
                
            ),
            color=discord.Color.green()
        )

        await canalTicket.send(
            content=f"{interaction.user.mention}",
            embed=embed,
            view=CloseTicketView()
        )

        await interaction.followup.send(
            f"✔️ **Ticket criado com sucesso, Visite o canal para ver o ticket clicando aqui `➡️`:** {canalTicket.mention}",
            ephemeral=True
        )

    elif tipo == 'sugestao':
        userid = interaction.user.id
        username = interaction.user.name
        problema = descricao
        cargo_id = None
        canal_id = None
        number_ticket = None
        armazenarDadosTicket(userid,username,tipo,problema,number_ticket,cargo_id,canal_id)


        
        webhook_url = getDadosSistema('c-solicitacoes-tickets')['data'][4]

        embed = discord.Embed(
            title=f"`🎫` Sugestão Aberta!",
            description=(
                f"`👤`**Usuário:** {interaction.user.mention}\n"
                f"**Tipo:** {tipo}\n\n"
                f"`💬`**Mensagem:**\n{descricao}"
            ),
            color=discord.Color.yellow()
        )

        webhook_url = getDadosSistema('c-solicitacoes-tickets')['data'][4]

        requests.post(webhook_url, json={
            "content": f"<@&{CEO}> <@&{STAFF}>",
            "embeds": [embed.to_dict()]
        })

        await interaction.followup.send(
            f"✔️ **Sugestão criada com sucesso, Obrigado pela sugestão!**",
            ephemeral=True
        )

    else:
        await interaction.followup.send('❌**Tipo de ticket inválido!**', ephemeral=True)

@bot.tree.command(name='help', description='Se precisar de ajuda relacionado ao mixcamp é so perguntar!')

async def teste(interaction: discord.Interaction, sobre: str):
    print(CEO, STAFF, MODERADOR, VERIFICADO, CATEGORIATICKETID)
# ------------------------------------------------
# ================= FUNÇÕES BASE ===========
# ------------------------------------------------

@bot.tree.command(name='configbase', description='Configuração base do bot poder funcionar.')
async def configBase(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    listaCargos = ['STAFF','Verificado','STREAMER','PASSE-LIVRE','MODERADOR']
    for roles in interaction.user.roles:
        

        if roles.name == '@everyone':
            pass
        else:
            role = roles.name.split('┇')[1].strip()
            if role in ['OWNER','STAFF','MODERADOR']:
                if role == 'OWNER':
                    verificarExiste = getDadosSistema('owner')

                    if verificarExiste['status']:
                        pass
                    else:
                        ArmazenarDadoSistema("cargos",roles.id,"owner","")

                for roles in interaction.guild.roles:
                    if roles.name == '@everyone':
                        pass
                    else:
                        role = roles.name.split('┇')[1].strip()

                        for cargo in listaCargos:
                            if role == cargo:
                                listaCargos.remove(cargo)
                            

                for cargo in listaCargos:
                    if cargo == 'STAFF':
                        
                        cargoStaff = await interaction.guild.create_role(
                            name="'⚙️┇STAFF",
                            colour=discord.Colour.orange(),
                            hoist=True,
                            mentionable=True,
                            permissions=discord.Permissions(administrator=True)
                        )
                        verificarExiste = getDadosSistema('staff')

                        if verificarExiste['status']:
                            pass
                        else:
                            ArmazenarDadoSistema("cargos",cargoStaff.id,"staff","")

                    if cargo == 'MODERADOR':
                        
                        cargoModerador = await interaction.guild.create_role(
                            name="'🛡️┇MODERADOR",
                            colour=discord.Colour.pink(),
                            hoist=True,
                            mentionable=True,
                            permissions=discord.Permissions(administrator=True)
                        )
                        verificarExiste = getDadosSistema('moderador')

                        if verificarExiste['status']:
                            pass
                        else:
                            ArmazenarDadoSistema("cargos",cargoModerador.id,"moderador","")

                        
                    if cargo == 'STREAMER':
                        cargoStreamer = await interaction.guild.create_role(
                            name="'🎥┇STREAMER",
                            colour=discord.Colour.purple(),
                            hoist=True,
                            mentionable=True,
                            permissions=discord.Permissions(administrator=False)
                        )
                        verificarExiste = getDadosSistema('streamer')

                        if verificarExiste['status']:
                            pass
                        else:
                            ArmazenarDadoSistema("cargos",cargoStreamer.id,"streamer","")

                    if cargo == 'PASSE-LIVRE':
                        cargoPasseLivre = await interaction.guild.create_role(
                            name="'💳┇PASSE-LIVRE",
                            colour=discord.Colour.yellow(),
                            hoist=False,
                            mentionable=True,
                            permissions=discord.Permissions(administrator=False)
                        )
                        verificarExiste = getDadosSistema('passelivre')
                        if verificarExiste['status']:
                            pass
                        else:
                            ArmazenarDadoSistema("cargos",cargoPasseLivre.id,"passelivre","")


                    if cargo == 'Verificado':
                        cargoVerificado = await interaction.guild.create_role(
                            name="'✔️┇Verificado",
                            colour=discord.Colour.green(),
                            hoist=True,
                            mentionable=True,
                            permissions=discord.Permissions(administrator=False)
                        )
                        verificarExiste = getDadosSistema('verificado')
                        if verificarExiste['status']:
                            pass
                        else:
                            ArmazenarDadoSistema("cargos",cargoVerificado.id,"verificado","")

                    await AtualizarIdCargos()

                await interaction.followup.send('✅**Sistema de configuração base criado com sucesso!**', ephemeral=True)
                break
            else:
                await interaction.followup.send('❌**Você não possui permissão para usar esse comando!**', ephemeral=True)

@bot.tree.command(name='createtables', description='Criar tabelas do banco de dados')
@app_commands.checks.has_any_role(CEO)
async def CreateTables(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)

    for roles in interaction.user.roles:
        

        if roles.name == '@everyone':
            pass
        else:
            role = roles.name.split('┇')[1].strip()
            if role in ['OWNER','STAFF']:
                
                status = criarTableDb()
                if status:
                    await interaction.followup.send("Tabelas criadas com sucesso!")
                else:
                    await interaction.followup.send("Erro ao criar tabelas!")
            else:
                await interaction.followup.send("❌**Você não possui permissão para usar esse comando!**")


@bot.tree.command(name="painel_link")
async def painel_link(interaction: discord.Interaction):

    embed = discord.Embed(
        title="**﹌﹌﹌﹌﹌﹌﹌`🔗`VINCULAR CONTA ﹌﹌﹌﹌﹌﹌﹌ **",
        description=(
            "**Para Liberar as salas do discord faça seu registro seguindo a passo a passo:**\n\n"
            "`1️⃣` **Acesse o site do MIXCAMP:\n https://mixcamp.online/frontend/html/login.html**\n"
            "`2️⃣` **acesse seu perfil e copia a url alguma coisa com final como:\n perfil.html?id=**\n"
            "`3️⃣` **No discord Clique no botão abaixo**\n"
            "`4️⃣` **Cole o link do seu Perfil**\n"
            "`5️⃣` **Envie o formulário**\n\n"
            "`⚠️` **Certifique-se de que o link está correto.**"
        ),
        color=discord.Color.blue()
    )

    await interaction.response.send_message(
        embed=embed,
        view=LinkView()
    )

# ------ REGISTRO DE CARGO DE TIME COM BASE NO SITE
@bot.tree.command(name='carregartime', description='Registrar cargo de time com base no site')
@app_commands.checks.has_any_role(CEO, STAFF)
async def CarregarCargosTimes(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)

    times = AtualizarCargoTimes()

    for time in times:
        cargo = await interaction.guild.create_role(
            name=f'.🥋┇ {time.upper()}',
            colour=discord.Colour.blue(),
            hoist=True,
            mentionable=True
        )

    await interaction.followup.send("✅ **Cargos de times carregados com sucesso!**", ephemeral=True)



# ------ LISTAR PARTIDAS MARCADAS
@bot.tree.command(name='veragendamentos', description="Listar todos os agendamentos ou o do dia atual ou da semana"
)

@app_commands.choices(
    periodo=[
        app_commands.Choice(name="Hoje", value="hoje"),
        app_commands.Choice(name="Essa semana", value="semana"),
        app_commands.Choice(name="Todas", value="todas")
    ]
)


async def mostrarPartidasMarcadas(interaction: discord.Interaction,periodo: app_commands.Choice[str]):
    if periodo.value not in ["hoje", "semana", "todas"]:
        await interaction.response.send_message("Período inválido ❌", ephemeral=True)
        return

    partidas = listarPartidasMarcadas(periodo.value)
    if partidas['status']:
        if periodo.value == 'hoje':
            complementar = 'de Hoje'
        elif periodo.value == 'semana':
            complementar = 'dessa Semana'
        elif periodo.value == 'todas':
            complementar = 'em breve'
        msg = f"**Olá {interaction.user.mention}! ✅ Partidas encontradas {complementar}:**\n"

        for item in partidas["dados"]:
            horario = item['horario'].split(':')
            horario = horario[0] + ':' + horario[1]
            msg += f"""
            ```
            =-=-=-=-=-=-=-=-🏆 MIXCAMP 🏆=-=-=-=-=-=-=-=-=-=
            🥊 Confronto: {item['time1'].upper()} 🆚 {item['time2'].upper()} 
            🕒 Horario: {horario}
            🆔 Data: {item['data']}
            ```
            """
        await interaction.response.send_message(msg, ephemeral=True)    

# ------ FERRAMENTA PARA AMISTOSO
@bot.tree.command(name='mix', description='Info: Nome do TIME 1, Nome do TIME 2, NOME DOS 10 PLAYERS')
async def mix(interaction: discord.Interaction, time1: str, time2: str, nomeplayer1: str,nomeplayer2: str,nomeplayer3: str,nomeplayer4: str,nomeplayer5: str,nomeplayer6: str,nomeplayer7: str,nomeplayer8: str,nomeplayer9: str,nomeplayer10: str):

    await interaction.response.defer(ephemeral=True)
    playersSemDefinir = [nomeplayer1,nomeplayer2,nomeplayer3,nomeplayer4,nomeplayer5,nomeplayer6,nomeplayer7,nomeplayer8,nomeplayer9,nomeplayer10]

    dados = PartidasAmistosaMix(playersSemDefinir)
    if dados['status']:
        playersDoTime1 = dados['playersDoTime1']
        playersDoTime2 = dados['playersDoTime2']
        embed = discord.Embed(
            title="🎮 Players separados aleatoriamente para o MIX",
            description=f"**{time1.upper()}** `🆚` **{time2.upper()}**",
            color=discord.Color.red()
        )

        embed.add_field(
            name=f"🔵 **{time1.upper()}**",
            value="\n".join([f"➥`🔷` **{player}**" for player in playersDoTime1]),
            inline=True
        )



        embed.add_field(
            name=f"🔴 **{time2.upper()}**",
            value="\n".join([f"➥`♦️` **{player}**" for player in playersDoTime2]),
            inline=True
        )

        embed.set_footer(text="MixCamp • Sistema de MIX")

        await interaction.followup.send(embed=embed,ephemeral=True)
        
    else:
        await interaction.followup.send("Erro ao gerar times amigáveis", ephemeral=True)



# ------------------------------------------------
# ================= SISTEMA DE TICKETS ===========
# ------------------------------------------------


@bot.tree.command(name="criarlocaladm", description="Criar sistema de admistração do discord")
@check_staff()
async def criarCategoriaTicket(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    guild = interaction.guild

    # CRIANDO CATEGORIA BEM VINDO E CANAIS
    categoria_bemvindos = await guild.create_category(f"ܔܔܢܜܔܢ🌎𝑩𝑬𝑴 𝑽𝑰𝑵𝑫𝑶🌎ܜܔܔܢܜ")
    canal_avisos = await guild.create_text_channel(
        "📢⡇𝐀𝐯𝐢𝐬𝐨𝐬",
        category=categoria_bemvindos,
        news=True
    )
    await canal_avisos.edit(type=discord.ChannelType.news)
    canal_avisos_webhook = await canal_avisos.create_webhook(name="MIXCAMP")
    canal_avisos_id = canal_avisos.id

    verificarExiste = getDadosSistema('c-avisos')
    if verificarExiste['status']:
        pass
    else:
        ArmazenarDadoSistema("canal",canal_avisos_id,"c-avisos",canal_avisos_webhook.url)

    canal_regras = await guild.create_text_channel("📕⡇𝐑𝐞𝐠𝐫𝐚𝐬", category=categoria_bemvindos)
    canal_regras_webhook = await canal_regras.create_webhook(name="MIXCAMP")
    canal_regras_id = canal_regras.id

    verificarExiste = getDadosSistema('c-regras')
    if verificarExiste['status']:
        pass
    else:
        ArmazenarDadoSistema("canal",canal_regras_id,"c-regras",canal_regras_webhook.url)

    canal_indentificacao = await guild.create_text_channel("🆔⡇𝑰𝒏𝒅𝒆𝒏𝒕𝒊𝒇𝒊𝒄𝒂𝒄𝒂𝒐", category=categoria_bemvindos)
    canal_indentificacao_webhook = await canal_indentificacao.create_webhook(name="MIXCAMP")
    canal_indentificacao_id = canal_indentificacao.id

    verificarExiste = getDadosSistema('c-indentificacao')
    if verificarExiste['status']:
        pass
    else:
        ArmazenarDadoSistema("canal",canal_indentificacao_id,"c-indentificacao",canal_indentificacao_webhook.url)

    canal_perfil = await guild.create_text_channel("👤⡇𝑷𝒆𝒓𝒇𝒊𝒍", category=categoria_bemvindos)
    canal_perfil_webhook = await canal_perfil.create_webhook(name="MIXCAMP")
    canal_perfil_id = canal_perfil.id

    verificarExiste = getDadosSistema('c-perfil')
    if verificarExiste['status']:
        pass
    else:
        ArmazenarDadoSistema("canal",canal_perfil_id,"c-perfil",canal_perfil_webhook.url)

    embed = discord.Embed(
        title="👤🔄 Painel de Perfil",
        description=(
            "Se houve algum tipo de mudança na sua conta, "
            "como mudança de time, nova medalha ou atualização "
            "de perfil, clique no botão abaixo para atualizar "
            "as informações exibidas no seu perfil do Discord."
        ),
        color=0x00BFFF
    )

    embed.set_footer(text="MIXCAMP • Sistema de Perfil")


    await canal_perfil.send(
        embed=embed,
        view=PainelPerfilView()
    )

    canal_chat = await guild.create_text_channel("💬⡇𝐆𝐞𝐫𝐚𝐥", category=categoria_bemvindos)
    canal_chat_webhook = await canal_chat.create_webhook(name="MIXCAMP")
    canal_chat_id = canal_chat.id

    verificarExiste = getDadosSistema('c-chat_geral')
    if verificarExiste['status']:
        pass
    else:
        ArmazenarDadoSistema("canal",canal_chat_id,"c-chat_geral",canal_chat_webhook.url)

    # criando_categoria_tickets e canal de abertura de tickets
    categoria = await guild.create_category(f"ܔܔܢܜܔܢ🔧𝑺𝒖𝒑𝒐𝒓𝒕🔧ܜܔܔܢܜ")
    canal = await guild.create_text_channel("🎫⡇𝐚𝐛𝐫𝐢𝐫-𝐭𝐢𝐜𝐤𝐞𝐭𝐬",category=categoria)

    CATEGORIATICKETID = categoria.id
    SALATICKET_ID = canal.id

    verificarExiste = getDadosSistema('ca-suport')

    if verificarExiste['status']:
        pass
    else:
        ArmazenarDadoSistema("categoria",CATEGORIATICKETID,"ca-suport","")
        
    verificarExiste = getDadosSistema('c-abrirtickets')
    webhook_abrirtickets = await canal.create_webhook(name="MIXCAMP")
    if verificarExiste['status']:
        pass
    else:
        ArmazenarDadoSistema("canal",SALATICKET_ID,"c-abrirtickets",webhook_abrirtickets.url)

    

    embed = discord.Embed(
        title="`🎫` **Sistema de Tickets**",
        description=(
            """
            **=-=-=-=-=-=-=-=-**`🏆` **MIXCAMP** `🏆`**=-=-=-=-=-=-=-=-=-=**\n
            **Selecione uma opção abaixo para abrir um ticket:**\n\n
            `📑` **Bug no site**\n
            `👮` **Reportar player**\n
            `⚙️` **Problemas técnicos**\n
            `📝` **Sugestões**\n
            `💬` **Dúvidas**
            **=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=**
            """
            
        ),
        color=discord.Color.blue()
    )
    embed.set_footer(text="MiXCAMP Suporte")

    await canal.send(embed=embed, view=TicketView())


    # criando_categoria_ranking e canal de ranking
    categoria_ranking = await guild.create_category(f"ܔܔܢܜܔܢ🏆 𝐂𝐀𝐌𝐏𝐄𝐎𝐍𝐀𝐓𝐎 🏆ܜܔܔܢܜ")
    canal_ranking = await guild.create_text_channel("📊⡇𝐫𝐚𝐧𝐤𝐢𝐧𝐠",category=categoria_ranking)
    webhook_ranking = await canal_ranking.create_webhook(name="MIXCAMP")

    verificarExiste = getDadosSistema('ca-ranking')

    if verificarExiste['status']:
        pass
    else:
        ArmazenarDadoSistema("categoria",categoria_ranking.id,"ca-ranking","")

    verificarExiste = getDadosSistema('c-ranking')

    if verificarExiste['status']:
        pass
    else:
        ArmazenarDadoSistema("categoria",canal_ranking.id,"c-ranking",webhook_ranking.url)


    

    

    # =============== CRIANDO CATEGORIA E CANAL DE ADMISTRACAO DO DISCORD ===============  

    cargo_ceo = guild.get_role(CEO)
    cargo_staff = guild.get_role(STAFF)
    cargo_moderador = guild.get_role(MODERADOR)

    overwrites = {
        guild.default_role: discord.PermissionOverwrite(view_channel=False),

        cargo_ceo: discord.PermissionOverwrite(
            view_channel=True,
            send_messages=True,
            read_message_history=True
        ),

        cargo_staff: discord.PermissionOverwrite(
            view_channel=True,
            send_messages=True,
            read_message_history=True
        ),

        cargo_moderador: discord.PermissionOverwrite(
            view_channel=True,
            send_messages=True,
            read_message_history=True
        )
    }

    

    # cria categoria com permissão
    categoria_adm = await guild.create_category(
        "ܔܔܢܜܔܢ 🔒👑𝙎𝙏𝘼𝙁𝙁👑🔒ܜܔܔܢܜ",
        overwrites=overwrites
    )
    verificarExiste = getDadosSistema('ca-staff')

    if verificarExiste['status']:
        pass
    else:
        ArmazenarDadoSistema("categoria",categoria_adm.id,"ca-staff","")

    # cria canal herdando permissões da categoria

    canal_logs = await guild.create_text_channel(
        "📑⡇𝙇𝙤𝙜𝙨",
        category=categoria_adm
    )

    webhook_tickets = await canal_logs.create_webhook(name="MIXCAMP")

    verificarExiste = getDadosSistema('c-logs')

    if verificarExiste['status']:
        pass
    else:
        ArmazenarDadoSistema("canal",canal_logs.id,"c-logs",webhook_tickets.url)



    canal_solicitacao_tickets = await guild.create_text_channel(
        "📩⡇𝙎𝙤𝙡𝙞𝙘𝙞𝙩𝙖𝙘𝙤𝙚𝙨-𝙩𝙞𝙘𝙠𝙚𝙩𝙨",
        category=categoria_adm
    )

    webhook_tickets = await canal_solicitacao_tickets.create_webhook(name="MIXCAMP")

    verificarExiste = getDadosSistema('c-solicitacoes-tickets')

    if verificarExiste['status']:
        pass
    else:
        ArmazenarDadoSistema("canal",canal_solicitacao_tickets.id,"c-solicitacoes-tickets",webhook_tickets.url)


    canal_adm_geral = await guild.create_text_channel(
        "💭⡇𝑪𝒉𝒂𝒕-𝑺𝒕𝒂𝒇𝒇",
        category=categoria_adm
    )

    verificarExiste = getDadosSistema('c-chat-staff')
    webhook_chat_staff = await canal_adm_geral.create_webhook(name="MIXCAMP")

    if verificarExiste['status']:
        pass
    else:
        ArmazenarDadoSistema("canal",canal_adm_geral.id,"c-chat-staff",webhook_chat_staff.url)

    canal_reuniao = await guild.create_voice_channel(
        "💬⡇𝑹𝒆𝒖𝒏𝒊𝒂𝒐",
        category=categoria_adm
    )
    verificarExiste = getDadosSistema('c-reuniao')
    webhook_reuniao = await canal_reuniao.create_webhook(name="MIXCAMP")
    if verificarExiste['status']:
        pass
    else:
        ArmazenarDadoSistema("canal",canal_reuniao.id,"c-reuniao",webhook_reuniao.url)


    canal_chegou = await guild.create_text_channel(
        "🚊⡇𝐂𝐡𝐞𝐠𝐨𝐮",
        category=categoria_adm
    )
    verificarExiste = getDadosSistema('c-chegou')
    webhook_chegou = await canal_chegou.create_webhook(name="MIXCAMP")
    if verificarExiste['status']:
        pass
    else:
        ArmazenarDadoSistema("canal",canal_chegou.id,"c-chegou",webhook_chegou.url)

    canal_vazou = await guild.create_text_channel(
        "🚀⡇𝐕𝐚𝐳𝐨𝐮",
        category=categoria_adm
    )
    verificarExiste = getDadosSistema('c-vazou')
    webhook_vazou = await canal_vazou.create_webhook(name="MIXCAMP")
    if verificarExiste['status']:
        pass
    else:
        ArmazenarDadoSistema("canal",canal_vazou.id,"c-vazou",webhook_vazou.url)

    await interaction.followup.send("✅**Sistema de ADMISTRAÇÃO do DISCORD criado com sucesso!**", ephemeral=True)


# ------ MARCAR HORARIO DA PARTIDA
@bot.tree.command(name='painelagendamento', description="Marca horário da partida entre equipes (ex: 19:00, 16/02/26, FURIA, MIBR)"
)
@check_staff()
async def painelAgendamento(interaction: discord.Interaction):

    embed = discord.Embed(
        title="📅 Sistema de Agendamento",
        description=(
            "**Selecione uma opção abaixo para agendar uma partida:**\n\n"
            "Clique no botão abaixo para agendar uma partida:"
            "`🕒` **Horário**\n"
            "`🆔` **Data**\n"
            "`🆔` **Equipe 1**\n"
            "`🆔` **Equipe 2**\n"
            "`🏆` **Campeonato**\n"
            "`🔍` **Season**\n"
        ),
        color=0xff6600
    )

    await interaction.response.send_message(
        embed=embed,
        view=PainelAgendamento()
        # ephemeral=True
    )

# ----------------------------------------------------------------------------------------------------------------------
# ====================================================== DISCORD PRINCIAPL =========================================================================
# ------------------------------------------------------------------------------------------------------------------------
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

# ------ INFO PLAYER MIXCAMP
@bot.tree.command(name='infoplayermix', description='buscar informações sobre o player no MixCamp. (Somente para admins e CEO)')

@app_commands.checks.has_any_role(CEO, STAFF)
async def infoPlayerMix(interaction: discord.Interaction, nickname: str):
    playerDados = playerMixcamp(nickname)
    if playerDados['status']:
        await interaction.response.send_message(f"""
        **Olá {interaction.user.mention}! ✅ Player localizado, informações abaixo:**
        ```
        =-=-=-=-=-=-=-=-🏆 MIXCAMP 🏆=-=-=-=-=-=-=-=-=-=
        🆔 Player ID: {playerDados['userDados']['usuario']['id']}
        🆔 Steam ID: {playerDados['userDados']['usuario']['steamid']}
        🆔 Faceit ID: {playerDados['userDados']['usuario']['faceitid']}
        👤 Nickname: {playerDados['userDados']['usuario']['username']}
        📧 Email: {playerDados['userDados']['usuario']['email']}
        📆 Data de Criação: {playerDados['userDados']['usuario']['data_criacao']}
        🎯 Posição: {playerDados['userDados']['usuario']['posicoes']}
        ⚔️ Gerencia: {playerDados['userDados']['usuario']['gerencia']}
        🎨 Cores de Perfil: {playerDados['userDados']['usuario']['cores_perfil']}
        ⚙️ Organizador: {playerDados['userDados']['usuario']['organizador']}
        =-=-=-=-=-=-=-=-🏆 TEAM 🏆=-=-=-=-=-=-=-=-=-=
        🆔 Time ID: {playerDados['userDados']['usuario']['time_id']}
        🥋 Time: {playerDados['userDados']['time']['nome']}
        🔖 Tag: {playerDados['userDados']['time']['tag']}
        =-=-=-=-=-=-=-=-🏆 REDES SOCIAIS 🏆=-=-=-=-=-=-=-=-=-=
        🔗 Discord: {playerDados['userDados']['redesSociais'][0]['discord_url']}
        🔗 YouTube: {playerDados['userDados']['redesSociais'][0]['youtube_url']}
        🔗 Instagram: {playerDados['userDados']['redesSociais'][0]['instagram_url']}
        🔗 Twitter: {playerDados['userDados']['redesSociais'][0]['twitter_url']}
        🔗 Twitch: {playerDados['userDados']['redesSociais'][0]['twitch_url']}
        🔗 Faceit: {playerDados['userDados']['redesSociais'][0]['faceit_url']}
        🔗 Gamesclub: {playerDados['userDados']['redesSociais'][0]['gamesclub_url']}
        🔗 Steam: {playerDados['userDados']['redesSociais'][0]['steam_url']}
        🔗 TikTok: {playerDados['userDados']['redesSociais'][0]['tiktok_url']}
        🔗 Kick: {playerDados['userDados']['redesSociais'][0]['kick_url']}
        🔗 Allstar: {playerDados['userDados']['redesSociais'][0]['allstar_url']}
        ```
        🖼 Avatar: {playerDados['userDados']['usuario']['avatar_url']}


        """, ephemeral=True)
    else:
        await interaction.response.send_message(f"""
        **Olá {interaction.user.mention}! ❌{playerDados['mensagem']}** """, ephemeral=True)






    
# ----------------------------------------------------------------------------------------------------------------------
# ====================================================== DISCORD DE TIMES =========================================================================
# ------------------------------------------------------------------------------------------------------------------------


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# ---------- SISTEMA DE CRIAR CANAIS
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

@bot.tree.command(name="painelcreatesalastimes", description="Painel para criar salas de times automáticas")
async def campeonatos_cmd(interaction: discord.Interaction):

    await interaction.response.send_message(
        "Painel de campeonatos:",
        view=PainelCampeonato()
    )
    


@bot.tree.command(name="deletarcanais", description="Deletar canais dos times do MIXCAMP")
@app_commands.checks.has_any_role(CEO, STAFF)
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
# ---------- START BOT
if __name__ == "__main__":
    bot.run(os.getenv("BotDicord"))