from discord.ext.commands import Cog
from discord.ext import tasks
from lib.bot import db


class Tasks(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db_auto_commit.start()

    @tasks.loop(seconds=45.0)
    async def db_auto_commit(self):
        db.commit()


def setup(bot):
    bot.add_cog(Tasks(bot))