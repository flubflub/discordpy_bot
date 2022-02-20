from asyncio import sleep
from discord.ext.commands import Bot as BotBase, CommandNotFound, Context, BadArgument, MissingRequiredArgument
from discord.errors import Forbidden
from discord import Intents

from lib.utility.time import timestamp
from lib.utility.console import printc
from lib.utility.bot import update_database, load_cogs, get_prefix

from config.settings import DISCORD_TOKEN
from config.settings import OWNER_IDS as OWNER_IDS
from config.settings import DEFAULT_BOT_LOGCHANNEL


class Bot(BotBase):
    def __init__(self):
        self.guild = None
        super().__init__(
            command_prefix=get_prefix,
            case_insensitive=True,
            owner_ids=OWNER_IDS,
            intents=Intents.all()
        )

    def setup(self):
        printc("[BOT]:", "setup ...", 50)
        load_cogs(self)
        printc("[BOT]:", "setup completed", 50)

    def run(self):
        self.setup()
        printc("[BOT]:", "starting ...", 50)
        super().run(DISCORD_TOKEN, reconnect=True)

    async def on_connect(self):
        printc("[BOT]:", "connected", 50)

    async def on_disconnect():
        printc("[BOT]:", "disconnected", 50)

    async def on_ready(self):
        self.botlog = self.get_channel(DEFAULT_BOT_LOGCHANNEL)
        update_database(self)
        await sleep(10)
        printc("[BOT]:", "start up complete", 50)
        await self.botlog.send(f":green_circle: {(await self.application_info()).name} is now online"
                                + f" Time:  {timestamp()}")

    async def process_commands(self, message):
        context = await self.get_context(message, cls=Context)
        if context.command is not None:
                await self.invoke(context)

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Something isn't working as expected")
            print(err, *args)

    async def on_command_error(self, ctx, err):
        ignored_errors = (BadArgument)
        if any([isinstance(err, error) for error in ignored_errors]):
            pass

        elif isinstance(err, CommandNotFound):
            await ctx.send("Command not found!")

        elif isinstance(err, MissingRequiredArgument):
            await ctx.send("Missing required argument(s)!")

        elif hasattr(err, "original"):
            if isinstance(err.original, Forbidden):
                await ctx.send("I do not have permission to do that.")
            else:
                raise err.original
        else:
            raise err

    async def on_message(self, message):
        if not message.author.bot:
            await self.process_commands(message)

bot = Bot()
