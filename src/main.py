import os
import bot
from lib.config import PREFIX

TOKEN = os.getenv('DISCORD_TOKEN')

bot = bot.Bot(command_prefix=PREFIX, prefix=PREFIX)

bot.run(TOKEN)