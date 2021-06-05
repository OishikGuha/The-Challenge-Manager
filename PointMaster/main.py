import os, random
import discord
from discord.ext import commands

import requests
import json, pickle


prefix = "get help"

def get_prefix(client, message): 
    global prefix
    with open(
         'prefixes.json', 'r'
    ) as f:  # open and read the prefixes.json, assuming it's in the same file
        prefixes = json.load(f)
        prefix = prefixes[str(message.guild.id)]  #load the json as prefixes
    return prefixes[str(
        message.guild.id)]  #recieve the prefix for the guild id give


client = commands.Bot(command_prefix=(get_prefix), case_insensetive=True)


class NewHelpName(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            emby = discord.Embed(description=page, colour=0xCCFF00)
            emby.set_footer(text= "Made by @NotSujal#1616. Current version is maintained by @Roboticol#4533. Version- 1.0")
            await destination.send(embed=emby)


client.help_command = NewHelpName()


def savedata(user, value):
    with open("data.tcm", 'rb') as f:
        data = pickle.load(f)

    data[user]= value
    with open("data.tcm", 'wb') as f:
        pickle.dump(data, f)


def createuser(user):
    if os.path.getsize("data.tcm") > 0:
        with open("data.tcm", 'rb') as f:
            data = pickle.load(f)
    else:
        data = {}
    data[user] = 0
    with open("data.tcm", 'wb') as f:
        pickle.dump(data, f)


def deletedata(user):
    with open("data.tcm", 'rb') as f:
        data = pickle.load(f)

    del data[user]
    with open("data.tcm", 'wb') as f:
        pickle.dump(data, f)


def getdata(user):
    with open("data.tcm", 'rb') as f:
        data = pickle.load(f)

        value = data[user]
    return value

#give command
@client.command(aliases= ["g"])
@commands.has_role("Challenge Creators")
@commands.cooldown(1,15)
async def give(ctx, mention: discord.User = None, points=0):
    """
    Give Points to a Member
    """
    user = mention.id

    try:
        player_pts = getdata(user)

    except:
        createuser(user)
        player_pts = 0

        pass
    player_pts += points
    savedata(user, player_pts)
    await ctx.send(f"Successfully added {points} points to {mention.mention}.")


@client.command(aliases= ["pts","p"])
@commands.cooldown(1, 20)
async def points(ctx, mention: discord.User = None):
    """
    View points of members
    """
    if mention == None:
        user = ctx.message.author.id
    else:
        user = mention.id

    player_pts = getdata(user)
    try:
        await ctx.send(
            f"{mention.mention} currently has **{player_pts}** points")
    except:
        await ctx.send(
            f"{ctx.message.author.mention} currently has **{player_pts}** points"
        )

#points error handler
@points.error
async def points_error_handler(ctx,error):
    await ctx.send(f"```{error}```")

#leaderboard command
@client.command(aliases= ["lb"])
@commands.cooldown(1,20)
async def leaderboard(ctx):
    """
    Leaderboard of the server
    """
    with open("data.tcm","rb") as f:
        data = pickle.load(f)
    emby = discord.Embed(title="Leaderboard",colour= 0xBEBEBE)
    
    rank =1
    txt = ''
    sort_orders = sorted(data.items(), key=lambda x: x[1], reverse=True)
    for i in sort_orders:
        #user = client.fetch_user(user)
        user = await client.fetch_user(int(i[0]))
        txt += "#" + str(rank) + "  " + str(user) + "  - "+ str(i[1]) + "\r\n"
        rank += 1
    emby.description = txt

    await ctx.send(embed = emby)

#Leaderboard error handler
@leaderboard.error
async def leaderboard_error_handler(ctx,error):
    await ctx.send(f"```{error}```")
#give command error
@give.error
async def givepoints_error_handler(ctx, error):
    await ctx.send(f"```{error}```")


@client.event
async def on_ready():
    global prefix
    print("Successfully Logged In!")

    activity = discord.Game(name="prefix is //", type=3)
    await client.change_presence(status=discord.Status.idle, activity=activity)


@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = '//'

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


@client.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

@client.command(aliases= ["latency"])
@commands.cooldown(1,5)
async def ping (ctx):
    await ctx.send(f"Pong!, latency {round(client.latency*1000)} ms")

#prefix command
@client.command()
@commands.is_owner()
@commands.cooldown(1, 20)
async def prefix(ctx, prefix):
    """
     Change the prefix of server
    """

    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    await ctx.send(f'Prefix changed to: {prefix}')

#error handleing for prefix
@prefix.error
async def prefix_error_handler(ctx, error):
    await ctx.send(f"```{error}```")

TOKEN = os.environ.get('TCM_TOKEN')
print(TOKEN)

client.run(TOKEN)
