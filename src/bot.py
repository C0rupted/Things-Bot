import os
import json
import requests
import discord

TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content == '!hello':
        await message.channel.send(f"Hello, @{message.author}")
    
    if message.content == "!meme":
        content = requests.get("https://meme-api.herokuapp.com/gimme/dankmemes").text
        data = json.loads(content)
        meme = discord.Embed(title=data['title'], url=data['postLink'])
        meme.set_image(url=f"{data['url']}")
        await message.channel.send(embed=meme)


client.run(TOKEN)