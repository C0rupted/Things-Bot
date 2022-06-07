import random
import discord
from discord.ext import commands

import lib.db as db

class Economy(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=["bal"])
    async def balance(self, ctx):
        """ Count your moolah! 🪙 """
        user = ctx.message.author
        data = await db.get_user(user)
        desc = f"  Wallet: {data[2]} 🪙 \n    Bank: {data[3]} 🪙 / {data[4]} 🪙"
        e = discord.Embed(title=f"{user.name}'s Moolah", description=desc,
                          color=discord.Color.green())
        await ctx.send(embed=e)
    
    @commands.command()
    @commands.cooldown(rate=1, per=3600.0, type=commands.BucketType.user)
    async def work(self, ctx):
        """ Earn some monies! """
        user = ctx.message.author

        income = random.randint(10, 50)

        desc = f"You worked for {income} 🪙!"
        e = discord.Embed(title=f"{user.name}'s Work", description=desc,
                          color=discord.Color.blue())

        await ctx.send(embed=e)

        data = await db.get_user(user)
        new_bal = str(int(data[2]) + income)
        await db.set_value(user, "wallet", new_bal)

    @commands.command()
    @commands.cooldown(rate=1, per=10.0, type=commands.BucketType.user)
    async def beg(self, ctx):
        """ Grovel in the hopes of getting some dough! """
        user = ctx.message.author

        income = random.randint(0, 5)

        if income == 0:
            desc = f"Your efforts were miserable. You earned 0 🪙."
            color = discord.Color.red()
        else:
            desc = f"You grovelled on your knees for {income} 🪙."
            color = discord.Color.dark_grey()

        e = discord.Embed(title=f"{user.name}'s Begging", description=desc,
                          color=color)

        await ctx.send(embed=e)

        data = await db.get_user(user)
        new_bal = str(int(data[2]) + income)
        await db.set_value(user, "wallet", new_bal)

    @commands.command(aliases=["dep"])
    @commands.cooldown(rate=1, per=3.0, type=commands.BucketType.user)
    async def deposit(self, ctx, amount):
        """ 💸 Keep your notes safe in the bank vault! 💸 """
        user = ctx.message.author
        data = await db.get_user(user)
        error = None

        if amount == "all":
            amount = data[2]
        else:
            amount = int(amount)

        if (int(data[3]) + amount) > int(data[4]):
            desc = f"""The bank denied your deposit of {amount} 🪙, because you \n
don't have enough space in your bank account."""
            error = True
        elif int(data[2]) < amount:
            desc = f"You don't have {amount} 🪙 in your wallet :("
            error = True
        else:
            desc = f"You deposited {amount} 🪙 into your bank account"

        e = discord.Embed(description=desc, color=discord.Color.green())
        await ctx.send(embed=e)
        if error:
            return

        data = await db.get_user(user)
        new_wallet_bal = str(int(data[2]) - amount)
        new_bank_bal = str(int(data[3] + amount))
        await db.set_value(user, "wallet", new_wallet_bal)
        await db.set_value(user, "bank_bal", new_bank_bal)

    @commands.command(aliases=["with"])
    @commands.cooldown(rate=1, per=3.0, type=commands.BucketType.user)
    async def withdraw(self, ctx, amount):
        user = ctx.message.author
        data = await db.get_user(user)
        error = None

        if amount == "all":
            amount = data[3]
        else:
            amount = int(amount)

        if amount > int(data[3]):
            desc = f"""The bank denied your withdrawal of {amount} 🪙, because \n
you don't have enough moolah in your account."""
            error = True
        else:
            desc = f"You withdrew {amount} 🪙 from your bank account"

        e = discord.Embed(description=desc, color=discord.Color.green())
        await ctx.send(embed=e)
        if error:
            return

        data = await db.get_user(user)
        new_wallet_bal = str(int(data[2]) + amount)
        new_bank_bal = str(int(data[3] - amount))
        await db.set_value(user, "wallet", new_wallet_bal)
        await db.set_value(user, "bank_bal", new_bank_bal)
    
    @commands.command()
    async def register(self, ctx):
        """ Get a free wallet and bank account """
        try:
            await db.register_user(ctx.message.author)
            await ctx.send("Enjoy your free stuff!")
        except:
            await ctx.send("Seems like you already have that stuff")