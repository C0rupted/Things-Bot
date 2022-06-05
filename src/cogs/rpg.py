import discord
from discord.ext import commands

import lib.db

class RPG(commands.Cog):
    def __init__(self, bot):
        """ Currently a WIP """
        self.bot = bot
