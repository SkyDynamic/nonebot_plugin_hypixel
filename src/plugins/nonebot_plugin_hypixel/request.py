from uuid import UUID
from httpx import AsyncClient

import requests
import re

client = AsyncClient()

class PlayerNameNotFound(Exception):
    pass

class HypixelAPICallError(Exception):
    pass

async def player_data(name: str, apikey):
    uuid = await get_uuid(name)
    return await get_player_data(uuid, apikey)

def checkPlayerName(player: str) -> bool:
    return (re.fullmatch(r"\w+",player) is not None) and len(player)<=16

async def get_uuid(player: str) -> UUID:
    '''获取MC UUID'''
    if not checkPlayerName(player):
        return None
    response = requests.get("https://api.mojang.com/users/profiles/minecraft/" + player)
    if response.status_code == 204:
        raise PlayerNameNotFound('未能找到此正版玩家')
    if response.status_code == 200:
        result = response.json()
        trimmedUUID=result['id']
        return UUID(trimmedUUID)

async def get_player_data(UUID: str, api_key: str) -> dict:
    initial_data = {}
    api = await client.get('https://api.hypixel.net/player',params={'key': api_key, 'uuid': UUID})
    Get_Call_Api_Status(api)
    initial_data['player'] = api.json().get('player')
    api = await client.get('https://api.hypixel.net/status',params={'key': api_key, 'uuid': UUID})
    Get_Call_Api_Status(api)
    initial_data['online'] = api.json().get('session').get('online')
    return initial_data

def Get_Call_Api_Status(api):
    if api.status_code == 400:
        raise HypixelAPICallError('不存在此玩家数据或丢失')
    if api.status_code == 403:
        raise HypixelAPICallError('缺少密钥或此密钥无效')
    if api.status_code == 429:
        raise HypixelAPICallError('超出API请求次数限制')
    if api.status_code == 200:
        pass