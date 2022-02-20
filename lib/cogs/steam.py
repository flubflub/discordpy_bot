import discord.ext.commands
from discord import Embed
from discord.ext.commands import Cog, command, BadArgument, guild_only
import lib.utility.steamapi as steamapi
from lib.utility.steam import steamid64_to_steamid, steamid64_to_steamid3, steamid_to_steamid64, steamid_to_steamid3, steamid3_to_steamid64, steamid3_to_steamid



class Steam(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name="steaminfo", aliases=["sinfo", "si", "steami"])
    async def steam_info(self, ctx, profile: str):
        idlist = await steamapi.get_steamid64(profile)
        # idlist [True, steamid64] or [False, ""]
        if idlist[0]:
            steamid64 = idlist[1]
            user_data = await steamapi.process_user_data(steamid64)
            print(user_data)
            embed = Embed(title="Steam Account",
                            description=f"**[{user_data['username']}]({user_data['profileurl']})**",
                            colour=0x546e7a)
            fields = [
                ("ID64", user_data["steamid"], True),
                ("ID3", steamid64_to_steamid3(user_data["steamid"]), True),
                ("ID", steamid64_to_steamid(user_data["steamid"]), True),
                ("CREATED", user_data["timecreated"], True),
                ("AVATAR", f"[LINK]({user_data['avatar']})", True)
            ]
            if (user_data["countrycode"] is not None) and (user_data["countrycode"] != "unknown"):
                fields.append(("COUNTRY", str(str(user_data["countrycode"])[2:])[:-2], True))
            if user_data["friends_amount"] != 0:
                fields.append(("FRIENDS", user_data["friends_amount"], True))
            if user_data["VACBanned"] is False:
                fields.append(("VAC BAN", f':green_square: {user_data["NumberOfVACBans"]}', True))
            elif user_data["VACBanned"] is True:
                fields.append(("VAC BAN", f':red_square: {user_data["NumberOfVACBans"]}', True))
            if user_data["NumberOfGameBans"] == 0:
                fields.append(("GAME BAN", f':green_square: {user_data["NumberOfGameBans"]}', True))
            elif user_data["NumberOfGameBans"] != 0:
                fields.append(("GAME BAN", f':red_square: {user_data["NumberOfGameBans"]}', True))
            if (user_data["VACBanned"] is True) or (user_data["NumberOfGameBans"] != 0):
                fields.append(("LAST BAN", f'{user_data["DaysSinceLastBan"]} days ago', True))
            if user_data["CommunityBanned"] is False:
                fields.append(("COMMUNITY BAN", f':green_circle: {user_data["CommunityBanned"]}', True))
            elif user_data["CommunityBanned"] is True:
                fields.append(("COMMUNITY BAN", f':red_circle: {user_data["CommunityBanned"]}', True))
            if user_data["EconomyBan"] == "none":
                fields.append(("ECONOMY BAN", f':green_circle: {user_data["EconomyBan"]}', True))
            elif user_data["EconomyBan"] != "none":
                fields.append(("ECONOMY BAN", f':red_circle: {user_data["EconomyBan"]}', True))
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            embed.set_thumbnail(url=user_data.get("avatar"))
            await ctx.send(embed=embed)
        elif not idlist[0]:
            await ctx.send(f"Can't find a steam account for {profile}."
                               f"\nPlease make sure to enter the correct format:"
                               f"```steaminfo <profile URL or custom URL>``` ")

    @steam_info.error
    async def steaminfo_error(self, context, exception):
        if isinstance(exception, BadArgument):
            await context.send("Can't get any information for this request")

    @command(name="steamidconvert", aliases=["sconvert", "steamid"])
    async def steamidconvert(self, ctx, sid: str):
        if sid.startswith("7"):
            await ctx.send(f"``SteamID:     {steamid64_to_steamid(int(sid))} \nSteamID3:    {steamid64_to_steamid3(int(sid))}``")
        elif sid.startswith("STEAM_"):
            await ctx.send(f"``SteamID64:     {steamid_to_steamid64(sid)} \nSteamID3:    {steamid_to_steamid3(sid)}``")
        elif sid.startswith("[U"):
            await ctx.send(f"``SteamID3:     {steamid3_to_steamid64(sid)} \nSteamID3:    {steamid3_to_steamid(sid)}``")
        else:
            raise BadArgument

    @steamidconvert.error
    async def steamidconvert_error(self, context, exception):
        if isinstance(exception, BadArgument):
            await context.send("Can't convert this ID!")



def setup(bot):
    bot.add_cog(Steam(bot))
