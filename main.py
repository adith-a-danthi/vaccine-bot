import discord
import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

TOKEN = os.environ.get('DISCORD_TOKEN')

client = discord.Client()


@client.event
async def on_ready():
    print(f'Logged in as ${client.user}')

client.run(TOKEN)
