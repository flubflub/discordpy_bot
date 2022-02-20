from discord.ext.commands import Cog, command, BadArgument, guild_only
from discord import Embed
from lib.utility.time import timestamp
import random
from lib.utility.chat import heads_or_tails, dog


class Chat(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="hi", aliases=["hello"])
    async def say_hi(self, ctx):
        await ctx.send(f"Hi {ctx.author.mention}")

    @command(name="echo", aliases=["say"])
    @guild_only()
    async def echo_message(self, ctx, *, message):
        await ctx.message.delete()
        await ctx.send(message)

    @command(name="is", aliases=["am", "are", "does", "do", "was", "were"])
    @guild_only()
    async def question_yes_no(self, ctx):
        response = random.randint(0, 1)
        if response == 0:
            await ctx.send("Yes.")
        elif response == 1:
            await ctx.send("No.")

    @command(name="coinflip", aliases=["flip", "coin"])
    @guild_only()
    async def coinflip(self, ctx):
        res = await heads_or_tails()
        await ctx.send(res.get("gif"))

    @command(name="dog")
    @guild_only()
    async def dog(self, ctx):
        res = await dog()
        embed = Embed(colour=0xa84300)
        embed.add_field(name="dog fact", value=res.get("fact"), inline=True)
        embed.set_image(url=res.get("image"))
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(Chat(bot))