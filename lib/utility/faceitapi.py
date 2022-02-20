from aiohttp import request
from config.settings import FACEIT_API_KEY


async def get_faceit_player_by_steamid64(steamid64):
    url = f"https://open.faceit.com/data/v4/players?game=csgo&game_player_id={steamid64}"
    async with request("GET", url, headers={'Authorization': FACEIT_API_KEY}) as res:
        if res.status == 200:
            result = await res.json()
            return [True, result]
        if res.status == 404:
            return [False, {}]


async def faceit_info_sum(steamid64: list, faceitdict: dict):
    for id in steamid64:
        data = await get_faceit_player_by_steamid64(id)
        if data[0]:
            faceitdict[id].update({
                "has_faceit": data[0],
                "nickname": data[1].get("nickname"),
                "level": data[1]["games"]["csgo"].get("skill_level"),
                "elo": data[1]["games"]["csgo"].get("faceit_elo")
            })
        elif not data[0]:
            faceitdict[id].update({
                "has_faceit": data[0],
                "elo": 0
                })
    return faceitdict
