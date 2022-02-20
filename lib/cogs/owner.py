from discord.ext.commands import Cog, command, is_owner
from discord import Activity, ActivityType, Streaming
from lib.bot import db
from lib.utility.time import timestamp
from lib.utility.console import printc

class Owner(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="close_connection", hidden=True)
    @is_owner()
    async def close_connection(self, ctx):
        db.commit()
        printc("[BOT]:", "manual disconnect", 50)
        await self.bot.botlog.send(f":red_circle: {(await self.bot.application_info()).name} had it's connection closed manually by {ctx.message.author}!"
                               + f" \n Time:  {timestamp()}")
        await self.bot.close()

    @command(name="change_activity", aliases=["ch_p"], hidden=True)
    @is_owner()
    async def change_activity(self, ctx, activitytype, *, activity):
        if activitytype == "listening":
            await self.bot.change_presence(activity=Activity(type=ActivityType.listening, name=activity))
        elif activitytype == "watching":
            await self.bot.change_presence(activity=Activity(type=ActivityType.watching, name=activity))
        elif activitytype == "playing":
            await self.bot.change_presence(activity=Activity(type=ActivityType.playing, name=activity))
        elif activitytype == "streaming":
            await self.bot.change_presence(activity=Streaming(name="Stream", url=activity))


def setup(bot):
    bot.add_cog(Owner(bot))
