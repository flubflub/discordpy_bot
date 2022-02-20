from aiohttp import request


async def heads_or_tails():
    url = f"https://no-api-key.com/api/v1/coin-flip"
    async with request("GET", url, headers={}) as res:
        if res.status == 200:
            result = await res.json()
            return result


async def dog():
    url = f"https://no-api-key.com/api/v1/animals/dog"
    async with request("GET", url, headers={}) as res:
        if res.status == 200:
            result = await res.json()
            return result