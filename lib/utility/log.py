from lib.bot import db


async def get_log_channel(self, id):
    return self.bot.get_channel(db.zelle("SELECT log_channel FROM guilds WHERE guild_id = ?", id))


async def get_log_channel_list(guild_list):
    guild_id_list = []
    for i in range(len(guild_list)):
        guild_id_list.append(guild_list[i].id)
    return guild_id_list


async def send_mult_log_channel(self, guild_id_list, embed):
    for id in guild_id_list:
        log_channel = await get_log_channel(self, id)
        await log_channel.send(embed=embed)