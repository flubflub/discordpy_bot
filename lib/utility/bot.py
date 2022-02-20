from lib.bot import db
from lib.utility.console import printc
from config.settings import COGS as COGS
from discord.ext.commands import when_mentioned_or


def load_cogs(bot):
    for cog in COGS:
        bot.load_extension(f"lib.cogs.{cog}")
        printc("[EXTENSION]:", f"{cog} loaded successfully", 0)


async def get_prefix(bot, msg):
    prefix = db.zelle("SELECT prefix FROM guilds WHERE guild_id = ?", msg.guild.id)
    return when_mentioned_or(prefix)(bot, msg)


def update_database(bot):
    db.execute_many("INSERT OR IGNORE INTO guilds (guild_id) VALUES (?)",
                 ((guild.id,) for guild in bot.guilds))
    printc("[DB]:", "guilds updated", 0)
    db.execute_many("INSERT OR IGNORE INTO users (discord_user_id) VALUES (?)",
                 ((member.id,) for guild in bot.guilds for member in guild.members if not member.bot))
    printc("[DB]:", "users updated", 0)
    db.commit()