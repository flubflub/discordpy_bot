from discord.ext.commands import Cog, command
from lib.utility.steam import steamid_to_steamid64
import lib.utility.steamapi as steamapi
import lib.utility.faceitapi as faceitapi
from discord import Embed
from collections import OrderedDict
from operator import getitem

class Csgo(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="checkfaceit", aliases=["cf"])
    async def checkfaceit(self, ctx, *, status):
        idlist = [s for s in status.split() if s.startswith('STEAM_')]
        id64list = []
        await ctx.message.delete(delay=3)
        await ctx.send("Processing ...", delete_after=5)
        async with ctx.typing():
            if len(idlist) <= 0:
                await ctx.send("Couldn't find any steam ids in this.")
            else:
                for id in idlist:
                    id64list.append(steamid_to_steamid64(id))
                idnamedict = await steamapi.get_name_and_id_from_sum(id64list)
                faceitdict = await faceitapi.faceit_info_sum(id64list, idnamedict)
                faceitdict = OrderedDict(sorted(faceitdict.items(), reverse=True,
                                         key=lambda x: getitem(x[1], 'elo')))
                embed = Embed(title="Faceit Check", colour=0xFF8C00)
                embed.set_thumbnail(url="https://assets.faceit-cdn.net/organizer_avatar/faceit_1551450699251.jpg")
                fields = []
                for id in faceitdict:
                    if faceitdict.get(id).get('has_faceit'):
                        fields.append((idnamedict.get(id).get('steam_name'),
                                        f"Faceit: **[{faceitdict.get(id).get('nickname')}](https://www.faceit.com/en/players/{faceitdict.get(id).get('nickname')}/stats/csgo)** \n"
                                        f"Level: **{faceitdict.get(id).get('level')}** \n"
                                        f"Elo: **{faceitdict.get(id).get('elo')}** \n"
                                                        , True))
                    elif not faceitdict.get(id).get('has_faceit'):
                        fields.append((idnamedict.get(id).get("steam_name"), f"**no faceit**", True))
                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)
                await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Csgo(bot))