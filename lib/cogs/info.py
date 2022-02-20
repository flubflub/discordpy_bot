from typing import Optional
from discord import Member, Embed
from discord.ext.commands import Cog, command, BadArgument


class Info(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="info")
    async def member_info(self, ctx, user: Optional[Member]):
        member = user or ctx.author
        embed = Embed(colour=member.color)
        fields = [
            ("NAME", f"{member.name}", True),
            ("DISKRIMINATOR", f"{member.discriminator}", True),
            ("DISPLAY NAME", f"{member.mention}", True),
            ("JOINED", f"{member.joined_at.strftime('%Y-%m-%d %H:%M:%S')}", True),
            ("CREATED", f"{member.created_at.strftime('%Y-%m-%d %H:%M:%S')}", True),
            ("TOP ROLE", f"{member.top_role.mention}", True),
            ("ACTIVITY", f"{member.activity}", True),
            ("IS BOT", f"{member.bot}", True),
            ("IS SYSTEM", f"{member.system}", True),
            ("ID", f"{member.id}", True),
            ("STATUS", f"{member.status}", True),
            ("DESKTOP STATUS", f"{member.desktop_status}", True),
            ("MOBILE STATUS", f"{member.mobile_status}", True),
            ("WEB STATUS", f"{member.web_status}", True),
            ("PENDING", f"{member.pending}", True),
            ("AVATAR URL", f"[LINK]({member.avatar_url})", True),
            ("ACTIVITIES", f"{member.activities}", True),
            ("ROLES", f"{', '.join([r.mention for r in member.roles if not r.is_default()])}", False),
        ]
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        embed.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=embed)

    @member_info.error
    async def member_info_error(self, ctx, err):
        if isinstance(err, BadArgument):
            await ctx.send("Can't find this Member!")

    @command(name="guildinfo")
    async def guild_info(self, ctx):
        embed = Embed(colour=0xf1c40f)
        fields = [
            ("NAME", f"{ctx.guild.name}", True),
            ("CREATED", f"{ctx.guild.created_at.strftime('%Y-%m-%d %H:%M:%S')}", True),
            ("MEMBERS", f"{ctx.guild.member_count}", True),
            ("REGION", f"{ctx.guild.region}", True),
            ("LOCALE", f"{ctx.guild.preferred_locale}", True),
            ("PREMIUM TIER", f"{ctx.guild.premium_tier}", True),
            ("BOOSTS", f"{ctx.guild.premium_subscription_count}", True),
            ("VERIFICATION", f"{ctx.guild.verification_level}", True),
            ("OWNER", f"{ctx.guild.owner.mention}", True),
            ("ID", f"{ctx.guild.id}", True),
            ("DESCRIPTION", f"{ctx.guild.description}", False),
            ("ROLES", f"{', '.join([r.mention for r in ctx.guild.roles if not r.is_default()])}", False),
        ]
        for name, value, inline in fields:
            embed.add_field(name=name, value=value, inline=inline)
        embed.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.send(embed=embed)

    @command(name="boost")
    async def boost(self, ctx, user: Optional[Member]):
        member = user or ctx.author
        if member.premium_since:
            await ctx.send(f"{member.mention} is boosting the Server since {member.premium_since}")
        else:
            await ctx.send(f"{member.mention} isn't boosting the Server")

    @member_info.error
    async def boost_error(self, ctx, err):
        if isinstance(err, BadArgument):
            await ctx.send("Can't find this Member!")


def setup(bot):
    bot.add_cog(Info(bot))