import discord
from discord.ext import commands
import discord
from dotenv import load_dotenv
import os
 
intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents = intents)
load_dotenv()
token  = os.getenv("TOKEN")

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    try:
        await client.load_extension('cogs.moderation')
        await client.load_extension('cogs.wordle')
        #await client.load_extension('cogs.tldrnews')
    except Exception as e:
        print(f'Failed to load extension: {e}')
 
@client.command()
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect()

@client.command()
async def leave(ctx):
    if ctx.voice_client is not None:
        await ctx.voice_client.disconnect()


client.run(token)