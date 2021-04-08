import discord
from discord.ext import commands
import requests
import json
import os

client = commands.Bot(command_prefix=">")

token = os.environ['CHALLENGEMANAGER_TOKEN']

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return quote 

@client.event
async def on_ready():
    print("{0.user} is ready!".format(client))
    print(get_quote())

@client.event
async def on_message(message):
    if message.author == client.user:
        return 

    if message.content.startswith("$quote"):    
        await message.channel.send(get_quote())

@client.command()
async def hello(ctx):
    await ctx.send("Hi")

client.run(token)