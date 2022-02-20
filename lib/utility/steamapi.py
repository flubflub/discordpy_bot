from config.settings import STEAM_API_KEY
from aiohttp import request
from lib.utility.time import convert_unix_time
import json


async def get_steamid64_from_customurl(customurl: str):
    URL = f"http://api.steampowered.com/ISteamUser/ResolveVanityURL/v0001/?key={STEAM_API_KEY}&vanityurl={customurl}&format=json"
    # {"response":{"steamid":"76561198073025954","success":1}}
    async with request("GET", URL, headers={}) as res:
        if res.status == 200:
            result = await res.json()
            return result["response"]["steamid"]


# https://steamcommunity.com/id/custom/ : fullcustomurl
# https://steamcommunity.com/profiles/0123456789 : profileurl
# custom : customurl
async def check_steamprofileurl(profile):
    # profile url
    if profile.startswith("https://steamcommunity.com/profiles/"):
        urlsplit = profile.split("/")
        return urlsplit[4]
    # full custom url
    elif profile.startswith("https://steamcommunity.com/id/"):
        urlsplit = profile.split("/")
        return await get_steamid64_from_customurl(urlsplit[4])
    # custom url
    else:
        return await get_steamid64_from_customurl(profile)


# returns list with index0: True or False (True when no error) and index1: the steamID64 or ""
async def get_steamid64(profile):
    try:
        steamid64 = await check_steamprofileurl(profile)
        return [True, steamid64]
    except:
        return [False, ""]


async def get_steam_player_summaries(steamid64):
    url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={STEAM_API_KEY}&steamids={steamid64}"
    async with request("GET", url, headers={}) as res:
        if res.status == 200:
            result = await res.json()
            return result


async def get_steam_friendlist(steamid64):
    url = f"https://api.steampowered.com/ISteamUser/GetFriendList/v1/?key={STEAM_API_KEY}&steamid={steamid64}&relationship=friend"
    async with request("GET", url, headers={}) as res:
        if res.status == 200:
            result = await res.json()
            return result


async def get_steam_bans(steamid64):
    url = f"https://api.steampowered.com/ISteamUser/GetPlayerBans/v1/?key={STEAM_API_KEY}&steamids={steamid64}"
    async with request("GET", url, headers={}) as res:
        if res.status == 200:
            result = await res.json()
            return result


def check_if_countrycode(user_data):
    if user_data['response']['players'][0].get('loccountrycode'):
        return True
    else:
        return False


def get_countrycode(user_data):
    if check_if_countrycode(user_data):
        return user_data['response']['players'][0].get('loccountrycode')
    else:
        return ""


def convert_steam_countrycode(countrycode):
    if countrycode == "":
        return
    else:
        json_data = json.loads(open('./data/steam/countries.json').read())
        return [x['name'] for x in json_data['countries'] if x['code'] == str(countrycode)]


async def count_steam_friends(steamid64):
    friends = await get_steam_friendlist(steamid64)
    if friends is None:
        return 0
    elif friends is not None:
        return len(friends['friendslist']['friends'])


async def add_non_public_info(refined_user_data, user_data):
    countrycode = convert_steam_countrycode(get_countrycode(user_data))
    timecreated = convert_unix_time(user_data['response']['players'][0].get('timecreated'))
    friends_amount = await count_steam_friends(user_data['response']['players'][0].get('steamid'))
    refined_user_data.update({"countrycode": countrycode})
    refined_user_data.update( {"timecreated": timecreated})
    refined_user_data.update({"friends_amount": friends_amount})
    return refined_user_data


async def add_steam_bans(steamid64, refined_user_data):
    baninfo = await get_steam_bans(steamid64)
    refined_user_data.update({"CommunityBanned": baninfo['players'][0].get("CommunityBanned")})
    refined_user_data.update({"VACBanned": baninfo['players'][0].get("VACBanned")})
    refined_user_data.update({"NumberOfVACBans": baninfo['players'][0].get("NumberOfVACBans")})
    refined_user_data.update({"DaysSinceLastBan": baninfo['players'][0].get("DaysSinceLastBan")})
    refined_user_data.update({"NumberOfGameBans": baninfo['players'][0].get("NumberOfGameBans")})
    refined_user_data.update({"EconomyBan": baninfo['players'][0].get("EconomyBan")})
    return refined_user_data


async def refine_user_data(user_data):
    refined_user_data = {
        "steamid": user_data['response']['players'][0].get('steamid'),
        "username": user_data['response']['players'][0].get('personaname'),
        "profileurl": user_data['response']['players'][0].get('profileurl'),
        "avatar": user_data['response']['players'][0].get('avatarfull'),
        "communityvisibilitystate": user_data['response']['players'][0].get('communityvisibilitystate'),
        "countrycode": "unknown",
        "timecreated": "unknown",
        "friends_amount": "unknown",
    }
    if refined_user_data.get('communityvisibilitystate') == 3:
        refined_user_data = await add_non_public_info(refined_user_data, user_data)
    return refined_user_data


async def process_user_data(steamid64):
    summary = await get_steam_player_summaries(steamid64)
    refined_user_data = await refine_user_data(summary)
    user_data = await add_steam_bans(steamid64, refined_user_data)
    return user_data


async def get_name_and_id_from_sum(id64list: list):
    iddict = {}
    data = await get_steam_player_summaries(id64list)
    for i in range(len(data['response']['players'])):
        iddict.update({
            int(data['response']['players'][i].get("steamid")): {
                "steam_name": data['response']['players'][i].get("personaname")
            }
        })
    return iddict


