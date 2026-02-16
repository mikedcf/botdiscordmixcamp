from db.db import conectar
from dotenv import load_dotenv
import requests
import os
load_dotenv()


def teste(texto):
    print(texto)


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
    

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# ---------- MIXCAMP
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=