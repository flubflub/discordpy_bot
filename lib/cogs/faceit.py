from discord.ext.commands import Cog, command
import lib.utility.faceitapi as faceitapi

class Faceit(Cog):
    def __init__(self, bot):
        self.bot = bot
        

def setup(bot):
    bot.add_cog(Faceit(bot))
