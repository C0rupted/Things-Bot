import discord

from discord.ext.commands import AutoShardedBot

from cogs.encryption import Encryption
from cogs.events import Events
from cogs.info import Information
from cogs.fun import Fun_Commands
from cogs.economy import Economy
from cogs.music import Music


class Bot(AutoShardedBot):
    def __init__(self, *args, prefix=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.prefix = prefix


    async def on_ready(self):
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching, name="!help"
            ),
            status=discord.Status.online
        )

        self.add_cog(Events(self))
        self.add_cog(Encryption(self))
        self.add_cog(Fun_Commands(self))
        self.add_cog(Information(self))
        self.add_cog(Economy(self))
        self.add_cog(Music(self))

        print("Logged in")

    async def on_message(self, msg):
        if not self.is_ready() or msg.author.bot:
            return

        await self.process_commands(msg)