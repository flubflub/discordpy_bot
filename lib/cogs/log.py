from datetime import datetime
from discord import Embed
from discord.ext.commands import Cog
from lib.bot import db
from lib.utility.time import embed as embed_timestamp
import lib.utility.log as log



class Log(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_member_join(self, member):
        db.execute("INSERT OR IGNORE INTO users (discord_user_id) VALUES (?)", member.id)
        log_channel = await log.get_log_channel(self, member.guild.id)
        embed = Embed(title=":blue_circle:      User joined",
                      colour=0x25A9FE,
                      description=f"**{member.name}#{member.discriminator}** has joined the server! ({member.id}) \n\n Account created: **{member.created_at.strftime('%d/%m/%Y %H:%M:%S')}**",
                      timestamp=datetime.utcnow())
        await log_channel.send(embed=embed)

    @Cog.listener()
    async def on_member_remove(self, member):
        log_channel = await log.get_log_channel(self, member.guild.id)
        embed = Embed(title=":red_circle:       User left",
                      colour=0xFE2525,
                      description=f"**{member.name}#{member.discriminator}** has left the server! ({member.id}) \n\n Nickname: **{member.nick}** \n Joined at: **{member.joined_at.strftime('%d/%m/%Y %H:%M:%S')}** \n Account created: **{member.created_at.strftime('%d/%m/%Y %H:%M:%S')}**",
                      timestamp=datetime.utcnow())
        await log_channel.send(embed=embed)

    @Cog.listener()
    async def on_user_update(self, before, after):
        log_channel_list = await log.get_log_channel_list(before.mutual_guilds)
        if before.name != after.name:
            embed = Embed(title=":bust_in_silhouette:       Username change",
                          colour=after.color,
                          timestamp=datetime.utcnow())
            fields = [("Before", f"**{before.name}#{before.discriminator}**", True),
                      ("After", f"**{after.name}#{after.discriminator}**", True)]
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            await log.send_mult_log_channel(self, log_channel_list, embed)
        if before.discriminator != after.discriminator:
            embed = Embed(title=":bust_in_silhouette:       Discriminator change",
                          colour=after.color,
                          timestamp=datetime.utcnow())
            fields = [("Before", f"**{before.name}#{before.discriminator}**", True),
                      ("After", f"**{after.name}#{after.discriminator}**", True)]
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            await log.send_mult_log_channel(self, log_channel_list, embed)
        if before.avatar_url != after.avatar_url:
            embed = Embed(title=":frame_photo:      Avatar change",
                          description=f"**{after.display_name}#{after.discriminator}** has changed their profile picture!",
                          colour=after.color,
                          timestamp=datetime.utcnow())
            fields = [("Before", f"[Link]({before.avatar_url})", True),
                      ("After", f"[Link]({after.avatar_url})", True)]
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            embed.set_thumbnail(url=before.avatar_url)
            embed.set_image(url=after.avatar_url)
            await log.send_mult_log_channel(self, log_channel_list, embed)

    @Cog.listener()
    async def on_member_update(self, before, after):
        log_channel = await log.get_log_channel(self, before.guild.id)
        if before.display_name != after.display_name:
            embed = Embed(title="Nickname change",
                          colour=after.colour,
                          timestamp=datetime.utcnow())
            fields = [("User", after.mention, True),
                      ("Before", before.display_name, True),
                      ("After", after.display_name, True)]
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            await log_channel.send(embed=embed)

        elif before.roles != after.roles:
            embed = Embed(title=f"Role updates for {before.name}#{before.discriminator}",
                          description=f"{after.mention}",
                          colour=after.colour,
                          timestamp=datetime.utcnow())
            if len(before.roles) == 1:
                before_field = ("Before", "No roles", False)
            elif len(before.roles) > 1:
                before_field = ("Before", ", ".join([r.mention for r in before.roles if not r.is_default()]), False)
            if len(after.roles) == 1:
                after_field = ("Before", "No roles", False)
            elif len(after.roles) > 1:
                after_field = ("After", ", ".join([r.mention for r in after.roles if not r.is_default()]), False)
            fields = [before_field, after_field]
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            await log_channel.send(embed=embed)

    @Cog.listener()
    async def on_message_edit(self, before, after):
        log_channel = await log.get_log_channel(self, before.channel.guild.id)
        if not after.author.bot:
            if before.content != after.content:
                embed = Embed(title="Message edit",
                              description=f"[Message]({after.jump_url}) edited by {after.author.mention}",
                              colour=after.author.colour,
                              timestamp=embed_timestamp())
                fields = [("Before", before.content, False),
                          ("After", after.content, False)]
                for name, value, inline in fields:
                    embed.add_field(name=name, value=value, inline=inline)
                await log_channel.send(embed=embed)

    @Cog.listener()
    async def on_message_delete(self, message):
        log_channel = await log.get_log_channel(self, message.channel.guild.id)
        # await self.bot.get_prefix(message) gibt list zurück weil definition siehe utility/bot.py
        # ['<@303340999910883330> ', '<@!303340999910883330> ', '.']
        # deswegen in tuple umwandeln, weil str.startswith() keine list nimmt nur tuple
        if (not message.author.bot) and (not message.content.startswith(tuple(await self.bot.get_prefix(message)))):
            embed = Embed(title="Message deletion",
                          description=f"Message sent by {message.author.mention}. \n It was sent at {message.created_at.strftime('%d/%m/%Y %H:%M:%S')}",
                          colour=message.author.colour,
                          timestamp=datetime.utcnow())
            fields = []
            if len(message.content) > 0:
                fields.append(("Content", message.content, False))
            else:
                fields.append(("Content", "No Content", False))
            if len(message.attachments) > 0:
                for i in range(len(message.attachments)):
                    fields.append(("Attachment ID", message.attachments[i].id, True))
                    fields.append(("Attachment Name", message.attachments[i].filename, True))
                    fields.append(("Attachment URL", message.attachments[i].url, True))
                embed.set_thumbnail(url=message.attachments[0].url)
            else:
                pass
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            await log_channel.send(embed=embed)

    @Cog.listener()
    async def on_member_ban(self, guild, user):
        log_channel = await log.get_log_channel(self, guild.id)
        embed = Embed(title=":no_entry:     User banned",
                      description=f"{user.name} ({user.id}) has been banned!",
                      colour=0xFF0000,
                      timestamp=datetime.utcnow())
        await log_channel.send(embed=embed)

    @Cog.listener()
    async def on_member_unban(self, guild, user):
        log_channel = await log.get_log_channel(self, guild.id)
        embed = Embed(title=":green_circle:     User unbanned",
                      description=f"**{user.name}#{user.discriminator}** ({user.id}) has been unbanned!",
                      colour=0x27FF00,
                      timestamp=datetime.utcnow())
        await log_channel.send(embed=embed)


def setup(bot):
	bot.add_cog(Log(bot))