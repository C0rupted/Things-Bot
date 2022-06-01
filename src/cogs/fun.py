import json
import random
import discord
import requests

from io import BytesIO
from discord.ext import commands
import urllib.request as request

from lib.data import eight_ball, bonk_objects


def list_to_text(list: list):
    text = ""
    for item in list:
        if item.index != (len(list)-1):
            text.join(f"\n{item},")
        else:
            text.join(f"\n{item}")
    return text

class Fun_Commands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["8ball"])
    @commands.cooldown(rate=1, per=2.0, type=commands.BucketType.user)
    async def eightball(self, ctx, *, question: commands.clean_content):
        """ Consult 8ball to receive an answer """

        answer = random.choice(eight_ball)
        await ctx.send(f"🎱 **Question:** {question}\n**Answer:** {answer}")

    @commands.command(aliases=["flip", "coin"])
    @commands.cooldown(rate=1, per=2.0, type=commands.BucketType.user)
    async def coinflip(self, ctx):
        """ Coinflip! """
        coinsides = ["Heads", "Tails"]
        await ctx.send(f"**{ctx.author.name}** flipped a coin and got **{random.choice(coinsides)}**!")

    @commands.command()
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
    async def randomfact(self, ctx):
        """ Bored? Learn some random facts """
        fact = request.urlopen("https://uselessfacts.jsph.pl//random.json?language=en")
        data = json.loads(fact.read().decode())
        embed = discord.Embed(title="🎲 Random Fact:",
                            description=data["text"],
                            color=discord.Color.random())
        await ctx.send(embed=embed)

    @commands.command(name="bonk", aliases=["hit"])
    @commands.cooldown(rate=1, per=10.0, type=commands.BucketType.user)
    async def bonk(self, ctx, member: str, *, reason = "no reason"):
        """'Bonk' someone with objects for specified reasons!"""
        if member == self.bot:
            await ctx.send(f"{ctx.author.mention} tried to bonk me, but I dodged them!")
        elif member == ctx.author.mention:
            await ctx.send(f"{ctx.author.mention} bonked themselves with {random.choice(bonk_objects)} for {reason}.")
        else:
            await ctx.send(f"{ctx.author.mention} bonked {member} with {random.choice(bonk_objects)} for {reason}.")


    @commands.command(name='quote')
    @commands.cooldown(rate=1, per=10.0, type=commands.BucketType.user)
    async def quote(self, ctx):
        """ Enlighten yourself with smart stuff from smart people """
        response = requests.get("https://zenquotes.io/api/random")
        json_data = json.loads(response.text)
        quote = json_data[0]["q"] + " -" + json_data[0]["a"]

        if quote == 'Too many requests. Obtain an auth key for unlimited access. -ZenQuotes.io':
            await ctx.send(
                "Do you seriously need more quotes? Wait 30 seconds please")
        else:
            await ctx.send(quote)

    @commands.command()
    @commands.cooldown(rate=1, per=2.0, type=commands.BucketType.user)
    async def reverse(self, ctx, *, text: str):
        """ !poow ,ffuts esreveR
        Everything you type after reverse will of course, be reversed
        """
        t_rev = text[::-1].replace("@", "@\u200B").replace("&", "&\u200B")
        await ctx.send(f"🔁 {t_rev}")

    @commands.command(aliases=["hotcalc", "hot"])
    async def howhot(self, ctx, *, user: discord.Member = None):
        """ Returns a random percent for how hot is a discord user """
        user = user or ctx.author

        random.seed(user.id)
        r = random.randint(1, 100)
        hot = r / 1.17

        if hot > 75:
            emoji = "💞"
        elif hot > 50:
            emoji = "💖"
        elif hot > 25:
            emoji = "❤"
        else:
            emoji = "💔"

        await ctx.send(f"**{user.name}** is **{hot:.2f}%** hot {emoji}")

    @commands.command()
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
    async def meme(self, ctx):
        """ Get some fast laughs """
        content = requests.get("https://meme-api.herokuapp.com/gimme").text
        data = json.loads(content)
        meme = discord.Embed(title=data['title'], url=data['postLink'], 
                            color=discord.Color.random())
        meme.set_image(url=f"{data['url']}")
        await ctx.send(embed=meme)
    
    @commands.command(aliases=["slots", "bet"])
    @commands.cooldown(rate=1, per=3.0, type=commands.BucketType.user)
    async def slot(self, ctx):
        """ Roll the slot machine """
        emojis = "🍎🍊🍐🍋🍉🍇🍓🍒"
        a, b, c = [random.choice(emojis) for g in range(3)]
        slotmachine = f"**[ {a} {b} {c} ]\n{ctx.author.name}**,"

        if (a == b == c):
            await ctx.send(f"{slotmachine} All matching, you won! 🎉")
        elif (a == b) or (a == c) or (b == c):
            await ctx.send(f"{slotmachine} 2 in a row, you won! 🎉")
        else:
            await ctx.send(f"{slotmachine} No match, you lost 😢")

