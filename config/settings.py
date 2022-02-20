import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
STEAM_API_KEY = os.getenv('STEAM_API_KEY')
FACEIT_API_KEY = os.getenv('FACEIT_API_KEY')
OWNER_IDS = []
DEFAULT_BOT_LOGCHANNEL = # add channel id


COGS = [
    'chat',
    'admin',
    'log',
    'info',
    'tasks',
    'owner',
    'steam',
    'csgo',
    'faceit',
]
