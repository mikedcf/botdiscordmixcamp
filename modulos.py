from db.db import conectar
from dotenv import load_dotenv
from datetime import datetime, timedelta
import requests
import os
import aiohttp
load_dotenv()



webhook_url_perfil = os.getenv('ROUTE_PERFIL_WEHOOK')

def PartidasAmistosaMix(playersSemDefinir):
# def PartidasAmistosaMix():
    contador = 0
    # playersSemDefinir = ['Lucas','João','Maria','Pedro','Ana','Bruno','Carla','Daniel','Eva','Fábio']
    playersDoTime1 = []
    playersDoTime2 = []
    
    try:
        import random
        while True:
            
            if contador >= 0 and contador < 5:
                player = random.choice(playersSemDefinir)
                playersDoTime1.append(player)
                playersSemDefinir.remove(player)
                contador += 1
            elif contador >= 5 and contador < 10:
                player = random.choice(playersSemDefinir)
                playersDoTime2.append(player)
                playersSemDefinir.remove(player)
                contador += 1
            else:
                break

        return {'status': True,
        'playersDoTime1': playersDoTime1,
        'playersDoTime2': playersDoTime2}
    except Exception as e:
        print(f"Erro: {e}")
        return False

# PartidasAmistosaMix()

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# ---------- FACEIT
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

def buscar_player(nickname):
    try:
        url = f"https://open.faceit.com/data/v4/players?nickname={nickname}"

        headers = {
            "Authorization": f"Bearer {os.getenv('ApiKeyFACEIT')}"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            level = data.get('games').get('cs2').get('skill_level')
            faceitId = data.get('player_id')
            steamId64 = data.get('steam_id_64')
            nickFaceit = data.get('nickname')
            nickSteam = data.get('steam_nickname')
            avatar = data.get('avatar')
            perfilFaceit = f'https://www.faceit.com/pt/players/{nickname}'

            playerDados = {
                'level': level,
                'faceitId': faceitId,
                'steamId64': steamId64,
                'nickFaceit': nickFaceit,
                'nickSteam': nickSteam,
                'avatar': avatar,
                'perfilFaceit': perfilFaceit,
                'status': True
            }

            return playerDados
            
            
        else:
            print(f"Erro: {response.status_code} - {response.json().get('message', 'Erro desconhecido')}")
            return False

    except Exception as e:
        print(f"Erro: {e}")
        return False

def hubFaceit(hub_uuid):
    try:
        url = f"https://open.faceit.com/data/v4/hubs/{hub_uuid}"

        headers = {
            "Authorization": f"Bearer {os.getenv('ApiKeyFACEIT')}"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            hubId = data.get('hub_id')
            name = data.get('name')
            avatar = data.get('avatar')
            coverImage = data.get('cover_image')
            gameId = data.get('game_id')
            region = data.get('region')
            description = data.get('description')
            chatRoomId = data.get('chat_room_id')
            organizerId = data.get('organizer_id')
            totalPlayers = data.get('players_joined')
            minSkillLevel = data.get('min_skill_level')
            maxSkillLevel = data.get('max_skill_level')
            joinPermission = data.get('join_permission')
            faceitUrl = data.get('faceit_url')

            hubDados = {
                'hubId': hubId,
                'name': name,
                'avatar': avatar,
                'coverImage': coverImage,
                'gameId': gameId,
                'region': region,
                'description': description,
                'chatRoomId': chatRoomId,
                'organizerId': organizerId,
                'totalPlayers': totalPlayers,
                'minSkillLevel': minSkillLevel,
                'maxSkillLevel': maxSkillLevel,
                'joinPermission': joinPermission,
                'faceitUrl': faceitUrl
            }

            return hubDados
        else:
            print(f"Erro: {response.status_code} - {response.json().get('message', 'Erro desconhecido')}")
            return False

    except Exception as e:
        print(f"Erro: {e}")
        return False

def membroHub(hub_uuid, nickname):
    nicknameTrue = False
    verifyNickname = buscar_player(nickname)
    if verifyNickname:
        try:
            url = f"https://open.faceit.com/data/v4/hubs/{hub_uuid}/members"

            headers = {
                "Authorization": f"Bearer {os.getenv('ApiKeyFACEIT')}"
            }

            response = requests.get(url, headers=headers)

            if response.status_code == 200:
                data = response.json()
                for item in data.get('items'):
                    if item.get('nickname') == nickname:
                        data = {
                            'nickname': item.get('nickname'),
                            'avatar': item.get('avatar'),
                            'roles': item.get('roles'),
                            'faceit_url': f'https://www.faceit.com/pt/players/{nickname}'
                        }
                        return {'status': True, 'data': data}
                
                if not nicknameTrue:
                    return {'status': False, 'mensagem': f'Não foi localizado o perfil do {nickname} na hub {hub_uuid}.'}
                
            else:
                print(f"Erro: {response.status_code} - {response.json().get('message', 'Erro desconhecido')}")
                return {'mensagem': 'Erro ao buscar membro do hub'}

        except Exception as e:
            print(f"Erro: {e}")
            return False
    else:
        return {'status': False, 'mensagem': f'Não foi localizado o perfil do {nickname} na Faceit.'}

def MatchFaceit(match_id):

    try:

        url = f"https://open.faceit.com/data/v4/hubs/{match_id}/matches"

        headers = {
            "Authorization": f"Bearer {os.getenv('ApiKeyFACEIT')}"
        }

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            data = response.json()
            nomeHub = data.get('items')[0]['competition_name']
            for item in data.get('items'):
                matchId = item['match_id']
                mapas = item['voting']['map']['pick']
                md = len(item['voting']['map']['pick'])
                status = item['status']
                
                dadosMatch = {
                    'nomeHub': nomeHub,
                    'matchId': matchId,
                    'mapas': mapas,
                    'md': f'MD{md}',
                    'status': status
                }
                return {'status': True, 'dados': dadosMatch}
        else:
            print(f"Erro: {response.status_code} - {response.json().get('message', 'Erro desconhecido')}")
            return {'status': False, 'mensagem': f'Erro ao buscar sobre filas.'}
    except Exception as e:
        print(f"Erro: {e}")
        return {'status': False, 'mensagem': f'Erro ao buscar sobre filas.'}
    
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# ---------- TABELAS
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
def teste():
    conectar("DROP TABLE usuarios_discord")


def criarTableDb():
    try:

        query = """ 
        CREATE TABLE IF NOT EXISTS usuarios_discord (
            id INTEGER PRIMARY KEY AUTOINCREMENT,

            userdiscordid INTEGER,
            usermixcampid INTEGER,

            username VARCHAR(50),
            usernamediscord VARCHAR(50),

            steamid INTEGER,
            faceitid VARCHAR(50),

            avatar_url VARCHAR(255),

            gerencia TEXT NOT NULL CHECK(gerencia IN ('admin', 'moderador', 'user', 'streamer')),

            organizador TEXT CHECK(organizador IN ('premium', 'simples', 'null')), 

            lider_id INTEGER DEFAULT NULL,

            nome_time VARCHAR(50) DEFAULT NULL,
            tag_time VARCHAR(50) DEFAULT NULL,

            avatar_time_url VARCHAR(255) DEFAULT NULL,

            funcao_no_time TEXT CHECK(
                funcao_no_time IN ('capitao', 'titular', 'reserva', 'coach')
            ) DEFAULT NULL,

            posicao_no_time TEXT CHECK(
                posicao_no_time IN ('awp', 'entry', 'support', 'igl', 'sub', 'coach', 'lurker', 'rifle','capitao')
            ) DEFAULT NULL,

            time_id INTEGER DEFAULT NULL,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        conectar(query)
       
        query = """ 
        CREATE TABLE IF NOT EXISTS sistema_discord (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT NOT NULL CHECK(tipo IN ('cargos', 'canal', 'categoria')),
            id_tipo INTEGER DEFAULT NULL,
            nome_tipo VARCHAR(255) NOT NULL,
            webhook_url TEXT DEFAULT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        conectar(query)

        query = """
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            userid INTEGER,
            username VARCHAR(50),
            tipo TEXT NOT NULL CHECK(tipo IN ('bug', 'report', 'tecnico', 'sugestao', 'duvidas')),
            problema TEXT,
            status BOOLEAN DEFAULT TRUE,
            number_ticket INTEGER,
            cargo_id INTEGER,
            canal_id INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        conectar(query)

        return True

    except Exception as e:
        return False

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# ---------- MIXCAMP
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

# -------- GET
def GetTimes():
    try:
        
        url = f'{os.getenv('ROUTE_MIXCAMP_API_TIMES')}'
        
        headers = {
            "x-api-key": os.getenv("ApiKeyMIXCAMP")
        }
        

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            
            return data['times']
        else:
            print('no')


    except Exception as e:
        print(f"Erro: {e}")
        return False

def DadosplayerID(id):
    try:
        
        url = f'{os.getenv('ROUTE_MIXCAMP_API_PERFIL')}{id}'
        headers = {
            "x-api-key": os.getenv("ApiKeyMIXCAMP")
        }
        

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return {'status': True, 'userDados': data}
        else:
            return {'status': False}

    except Exception as e:
        print(f"Erro: {e}")
        return {'status': False}

def getDadosUserCompleto(idMixcamp):
    try:
        url = f'{os.getenv('ROUTE_MIXCAMP_API_USER_COMPLETO')}{idMixcamp}'
        headers = {
            "x-api-key": os.getenv("ApiKeyMIXCAMP")
        }
    
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            print('ok')
            return {'status': True, 'data': response.json()}
        else:
            print(response.json())
            return {'status': False}
    except Exception as e:
        print(f"Erro: {e}")
        return {'status': False}

def getSeasons():
    try:
        url = f'{os.getenv('ROUTE_MIXCAMP_API_SEASONS')}'
        headers = {
            "x-api-key": os.getenv("ApiKeyMIXCAMP")
        }
        

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return {'status': True, 'data': response.json()}
        else:
            return {'status': False}
    except Exception as e:
        print(f"Erro: {e}")
        return {'status': False}

def getAgendamentos():
    try:
        url = f'{os.getenv('ROUTE_MIXCAMP_API_AGENDAMENTOS')}'
        headers = {
            "x-api-key": os.getenv("ApiKeyMIXCAMP")
        }
    
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return {'status': True, 'data': response.json()}
        else:
            return {'status': False}
    except Exception as e:
        print(f"Erro: {e}")
        return {'status': False}

def playerMixcamp(nickname):
    try:
        url = os.getenv('ROUTE_MIXCAMP_API_USERS_ALL')
        headers = {
            "x-api-key": os.getenv("ApiKeyMIXCAMP")
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            for userDados in data:
                if userDados['username'] == nickname:
                    user = DadosplayerID(userDados['id'])
                    if user['status']:
                        return {"status": True, "userDados": user['userDados']}
                    else:
                        return {"status": False, "mensagem": "Erro ao buscar dados do player"}
        else:
            return {"status": False, "mensagem": "Erro ao buscar dados do player"}
        

    except Exception as e:
        print(f"Erro: {e}")
        return {'status': False, 'mensagem': f'Erro: {e}'}


# -------- POST


# -------- PUT


# -------- DELETE


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# ---------- DISCORD
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# -------- GET
def getDadosSistema(tipo): 
    try:
        query = f"SELECT * FROM sistema_discord WHERE nome_tipo = ?"
        response = conectar(query, (tipo,))
        return {'status': True, 'data': response[0]}

    except Exception as e:
        return {'status': False}

def getNumeroTicket():
    try: 
        query = f"SELECT MAX(number_ticket) FROM tickets"
        response = conectar(query)
        
        return {'status': True, 'data': response[0][0]}
    except Exception as e:
        return {'status': False}

def getDadosTicket(coluna,valor):
    try:
        query = f"SELECT * FROM tickets WHERE {coluna} = ?"
        response = conectar(query, (valor,))
        return {'status': True, 'data': response[0]}
    except Exception as e:
        return {'status': False}

def getDadosUserDiscord(userId):
    try:
        query = f"SELECT * FROM usuarios_discord WHERE userdiscordid = ?"
        response = conectar(query, (userId,))
        return {'status': True, 'data': response[0]}
    except Exception as e:
        print(f"Erro: {e}")
        return {'status': False}


# -------- POST
def ArmazenarDadoSistema(cargo,canal,categoria,webhook):
    try:
        conectar('INSERT INTO sistema_discord (tipo,id_tipo,nome_tipo,webhook_url) VALUES (?,?,?,?)',(cargo,canal,categoria,webhook))
        return True
    except Exception as e:
        return False

def armazenarDadosTicket(userid,username,tipo,problema,number_ticket,cargo_id,canal_id):
    try:
        query = f"INSERT INTO tickets (userid,username,tipo,problema,number_ticket,cargo_id,canal_id) VALUES (?,?,?,?,?,?,?)"
        conectar(query, (userid,username,tipo,problema,number_ticket,cargo_id,canal_id))
        return True
    except Exception as e:
        return False

def ArmazenarDadosUserDiscord(userdiscordid,usermixcampid,username,usernamediscord,steamid,faceitid,avatar_url,gerencia,organizador='',lider_id=None,nome_time=None,tag_time=None,avatar_time_url=None,funcao_no_time=None,posicao_no_time=None,time_id=None):
    try:
        if lider_id == None:
            query = f"INSERT INTO usuarios_discord (userdiscordid,usermixcampid,username,usernamediscord,steamid,faceitid,avatar_url,gerencia,organizador) VALUES (?,?,?,?,?,?,?,?,?)"
            conectar(query, (userdiscordid,usermixcampid,username,usernamediscord,steamid,faceitid,avatar_url,gerencia,organizador))
        else:
            query = f"INSERT INTO usuarios_discord (userdiscordid,usermixcampid,username,usernamediscord,steamid,faceitid,avatar_url,gerencia,organizador,lider_id,nome_time,tag_time,avatar_time_url,funcao_no_time,posicao_no_time,time_id) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
            conectar(query, (userdiscordid,usermixcampid,username,usernamediscord,steamid,faceitid,avatar_url,gerencia,organizador,lider_id,nome_time,tag_time,avatar_time_url,funcao_no_time,posicao_no_time,time_id))

        return True
    except Exception as e:
        print(f"Erro: {e}")
        return False

def AmarzenarAgendamento(idMixcamp,primeiroTime,segundoTime,dataJogo,horario,season,campeonatos):

    from datetime import datetime

    if len(dataJogo) == 8:
        dataJogo = dataJogo.split('/')
        dataJogo = dataJogo[0] +'/'+ dataJogo[1] +'/'+ f'20{dataJogo[2]}'

    data = dataJogo


    nova_data = datetime.strptime(data, "%d/%m/%Y").strftime("%Y/%m/%d")


    try: 
        url = os.getenv('ROUTE_MARCACOES_JOGOS_CRIAR')
        headers = {
            "x-api-key": os.getenv("ApiKeyMIXCAMP")
        }
        response = requests.post(url, json={
            'usuario_id': idMixcamp,
            'primeiro_time_nome': primeiroTime,
            'segundo_time_nome': segundoTime,
            'horario_inicio': horario,
            'campeonatos': campeonatos,
            'season': season,
            'data_do_jogo': nova_data
        }, headers=headers)
        if response.status_code == 200:
            return {'status': True, 'data': response.json()}
        else:
            return {'status': False, 'mensagem': response.json().get('message', 'Erro desconhecido')}
    except Exception as e:
        print(f"Erro: {e}")
        return {'status': False, 'mensagem': f'Erro: {e}'}

# -------- PUT
def AtualizarDadosTicket(numberTicket,status):

    try:
        query = f"UPDATE tickets SET status = ? WHERE number_ticket = ?"
        conectar(query, (status,numberTicket))
        return True
    except Exception as e:
        return False

def atualiiarDadosUserDiscord(coluna,valor,id):
    try:
        query = f"UPDATE usuarios_discord SET {coluna} = ? WHERE id = ?"
        conectar(query, (valor,id))
        return True
    except Exception as e:
        print(f"Erro: {e}")
        return False


# -------- DELETE



# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# ---------- FUNÇÕES
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

def converter_data(data_iso):
    data = datetime.fromisoformat(data_iso.replace("Z", "+00:00"))
    return data.strftime("%d/%m/%Y")


def horaDate():
    from datetime import datetime
    import requests

    url = "https://timeapi.io/api/Time/current/zone?timeZone=America/Sao_Paulo"
    data = requests.get(url).json()

    dt = datetime.fromisoformat(data["dateTime"])
    data = dt.strftime("%d/%m/%Y")

    hora = dt.strftime("%H:%M:%S")
    return {'data': data, 'hora': hora}

def Verificar_extrairID(url):

    extration = url.split('/')
    verificarPerfilUrl = extration[-1].split('?')[0]
    if verificarPerfilUrl == 'perfil.html':
        idPerfil = extration[-1].split('?')[1].split('=')[1]

        return {'status': True, 'id': idPerfil}
    else:
        return {'status': False}

def listarPartidasMarcadas(periodo):
    
    dadosPartidas = []
    try:
        dados = getAgendamentos()

        if periodo == 'hoje':
            dataHoje = horaDate()['data']
            for dado in dados['data']['marcacoesJogos']:
                if dado['data_do_jogo'] == None:
                    pass
                else:
                    if converter_data(dado['data_do_jogo']) == dataHoje:
                        usuarioRegistro = dado['usuario_id']
                        time1 = dado['primeiro_time_nome']
                        time2 = dado['segundo_time_nome']
                        horario = dado['horario_inicio']
                        data = dataHoje
                        season = dado['season']
                        campeonatos = dado['campeonatos']

                        dadosPartidas.append({'usuarioRegistro': usuarioRegistro, 'time1': time1, 'time2': time2, 'horario': horario, 'data': data, 'season': season, 'campeonatos': campeonatos})
                        break
            return {'status': True, 'dados': dadosPartidas}

        elif periodo == 'semana':
            dataHoje = horaDate()['data']
            dataHoje = datetime.strptime(dataHoje, '%d/%m/%Y')

            # segunda-feira
            inicioSemana = dataHoje - timedelta(days=dataHoje.weekday())
            # domingo
            fimSemana = inicioSemana + timedelta(days=6)


            inicioSemana = inicioSemana.strftime('%d/%m/%Y')
            fimSemana = fimSemana.strftime('%d/%m/%Y')


            for dado in dados['data']['marcacoesJogos']:
                if dado['data_do_jogo'] == None:
                    pass
                else:
                    if converter_data(dado['data_do_jogo']) >= inicioSemana and converter_data(dado['data_do_jogo']) <= fimSemana:
                        usuarioRegistro = dado['usuario_id']
                        time1 = dado['primeiro_time_nome']
                        time2 = dado['segundo_time_nome']
                        horario = dado['horario_inicio']
                        data = converter_data(dado['data_do_jogo'])
                        season = dado['season']
                        campeonatos = dado['campeonatos']
                        dadosPartidas.append({'usuarioRegistro': usuarioRegistro, 'time1': time1, 'time2': time2, 'horario': horario, 'data': data, 'season': season, 'campeonatos': campeonatos})

            return {'status': True, 'dados': dadosPartidas}


        elif periodo == 'todas':
            dataHoje = horaDate()['data']

            for dado in dados['data']['marcacoesJogos']:
                if dado['data_do_jogo'] == None:
                    pass
                else:
                    if converter_data(dado['data_do_jogo']) >= dataHoje:
                        usuarioRegistro = dado['usuario_id']
                        time1 = dado['primeiro_time_nome']
                        time2 = dado['segundo_time_nome']
                        horario = dado['horario_inicio']
                        data = converter_data(dado['data_do_jogo'])
                        season = dado['season']
                        campeonatos = dado['campeonatos']
                        dadosPartidas.append({'usuarioRegistro': usuarioRegistro, 'time1': time1, 'time2': time2, 'horario': horario, 'data': data, 'season': season, 'campeonatos': campeonatos})

        return {'status': True, 'dados': dadosPartidas}

        
    except Exception as e:
        print(f"Erro: {e}")
        return {'status': False, 'mensagem': f'Erro: {e}'}


# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
criarTableDb()