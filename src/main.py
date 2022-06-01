import os
import bot

TOKEN = os.getenv('DISCORD_TOKEN')

bot = bot.Bot(command_prefix='!', prefix='!')

bot.run(TOKEN)