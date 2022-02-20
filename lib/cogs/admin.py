from discord.ext.commands import Cog, command, is_owner, BadArgument, has_permissions, guild_only
from lib.bot import db


class Admin(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="set_prefix", hidden=True)
    @guild_only()
    @has_permissions(manage_guild=True)
    async def set_prefix(self, ctx, prefix: str):
        if prefix.isascii() and len(prefix) <= 3:
            db.execute("UPDATE guilds SET prefix = ? WHERE guild_id = ?", prefix, ctx.message.guild.id)
            await ctx.send(f"Command prefix has been changed to ``{prefix}``")
        else:
            await ctx.send("The prefix can't be longer than 3 characters and those must be ASCII.")

    @set_prefix.error
    async def set_prefix_error(self, ctx, err):
        if isinstance(err, BadArgument):
            await ctx.send('Bad Argument')


    @command(name="set_log", hidden=True)
    @guild_only()
    @has_permissions(manage_guild=True)
    async def set_log(self, ctx, channel_id: int):
        db.execute("UPDATE guilds SET log_channel = ? WHERE guild_id = ?", channel_id, ctx.message.guild.id)
        await ctx.send(f"Log channel has been set to {channel_id}.")

    @set_log.error
    async def set_log_error(self, ctx, err):
        if isinstance(err, BadArgument):
            await ctx.send('This is not a channel id!')

    @command(name="latency", hidden=True)
    @has_permissions(manage_guild=True)
    async def check_latency(self, ctx):
        await ctx.send(f'Responded within {"{:0.8f}".format(self.bot.latency)} seconds.')

    @command(name="activity", hidden=True)
    @has_permissions(manage_guild=True)
    async def check_activity(self, ctx):
        await ctx.send(f"Bot activity: {self.bot.activity}")

    @command(name="emojis", hidden=True)
    @guild_only()
    @has_permissions(manage_guild=True)
    async def check_emojis(self, ctx):
        await ctx.send(f"Bot has access to these emojis: {self.bot.emojis}")


def setup(bot):
    bot.add_cog(Admin(bot))