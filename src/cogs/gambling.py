import random
import discord
from discord.ext import commands
from discord import ActionRow, Button, ButtonStyle

import lib.db as db
from lib.data import russian_roulette_bang, russian_roulette_click, russian_roulette_start


class Gambling(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    @commands.cooldown(rate=1, per=30.0, type=commands.BucketType.user)
    async def slot(self, ctx, amount: int):
        """ 🪙🪙🪙 Gamble the slot machine for dough! 🪙🪙🪙 """
        user = ctx.message.author
        data = await db.get_user(user)
        emojis = "🍋🥕🍎🍌🍑🍅🍊🍐🍉🍇🍓🍒"

        a, b, c = [random.choice(emojis) for g in range(3)]
        prefix = f"**[{a} {b} {c}]**\n"
        color = discord.Color.green()
        if (a == b == c):
            income = amount * 5
            desc = f"""{prefix}You **WON**! Do you know how rare that is!?!\n
You earned {income} 🪙."""
        elif (a == b) or (a == c) or (b == c):
            income = amount * 1
            desc = f"""{prefix}You **WON**! You earned {income} 🪙."""
        else:
            income = amount * -1
            desc = f"""{prefix}You **LOST**! You shouldn't have bet all that money. :(\n
You lost {str(income).replace('-', '')} 🪙."""
            color = discord.Color.red()

        if int(data[2]) < amount:
            desc = """You don't own that many notes! You're lucky, I saved you from debt."""
            color = discord.Color.red()

        e = discord.Embed(title=f"{user.name} Gambling the Slot", description=desc,
                          color=color)
        await ctx.send(embed=e)

        new_bal = str(int(data[2]) + income)
        await db.set_value(user, "wallet", new_bal)

    @commands.command(aliases=["roulette", "roul"])
    @commands.cooldown(rate=1, per=30.0, type=commands.BucketType.user)
    async def russianroulette(self, ctx, bullets: int):
        """ 🪙 Try your chances of not shooting yourself! 💀 """
        user = ctx.message.author
        data = await db.get_user(user)
        money = bullets * 100

        components = [ActionRow(Button(label="Spin!",
                                        custom_id="spin",
                                        style=ButtonStyle.blurple)),
        ]

        if bullets > 5:
            desc = "Sorry dude, but if you have more than 5 bullets, then there's no way for you to win!"
            components = None
        elif int(data[2]) < money:
            desc = f"Sorry dude, but you don't have {money} 🪙 on you at the moment, no way am I gambling with you!"
        else:
            desc = russian_roulette_start
            chambers = ["empty", "empty", "empty", "empty", "empty", "empty"]
            filled = []
            temp = 0
            for i in range(0, bullets):
                while temp in filled:
                    temp = random.randint(0, 5)
                chambers[temp] = "bullet"
                filled.append(temp)

        e = discord.Embed(title=f"{user.name} Playing Russian Roulette", description=desc,
                          color=discord.Color.dark_grey())
        msg = await ctx.send(embed=e, components=components)

        def _check(i: discord.ComponentInteraction, b):
            return i.message == msg and i.member == ctx.author

        interaction, button = await self.bot.wait_for('button_click', check=_check)

        if chambers[random.randint(0, 5)] == "bullet":
            desc = russian_roulette_bang
            color = discord.Color.red()
        else:
            desc = russian_roulette_click
            color = discord.Color.green()
        
        components = [components[0].disable_all_buttons()]
        edited_embed = e
        e.description = desc
        e.color = color
        await interaction.edit(embed=edited_embed, components=components)

        if desc == russian_roulette_bang:
            await ctx.send(f"""Oooh! Bad Luck! Unfortunately you shot yourself, so I'm going to have to take 
{money} 🪙 from you.""")
            new_bal = str(int(data[2]) - money)

        else:
            await ctx.send(f"Wow! You managed not to die! To show my support, here is {money} 🪙.")
            new_bal = str(int(data[2]) + money)
        await db.set_value(user, "wallet", new_bal)

