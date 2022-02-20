from discord.ext.commands import Cog, command
import lib.utility.faceitapi as faceitapi

class Faceit(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="faceitplayer", aliases=["fp"])
    async def faceitplayer(self, ctx, steamid64):
        r = await faceitapi.faceit_info_sum()
        print(r)


def setup(bot):
    bot.add_cog(Faceit(bot))