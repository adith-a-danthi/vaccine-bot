import discord
import os
from dotenv import load_dotenv
from discord.ext import tasks, commands
from datetime import datetime
from utils import get_slot_details, filter_response

load_dotenv()

TOKEN = os.environ.get('DISCORD_TOKEN')
CHANNEL_ID = os.environ.get('CHANNEL_ID')
DISTRICT_ID = os.environ.get('DISTRICT_ID')
MIN_AGE = os.environ.get('MIN_AGE')

client = discord.Client()


@client.event
async def on_ready():
    print(f'Logged in as ${client.user}')
    send_embed.start()


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('_ping'):
        await message.channel.send(f'Pong! `{round(client.latency * 1000)}ms`')


@tasks.loop(minutes=5)
async def send_embed():
    response, failed = get_slot_details(district_id=DISTRICT_ID)
    if failed:
        print('Error fetching slots')
        return
    if response == []:
        print('No slots available')
        return

    channel = client.get_channel(id=int(CHANNEL_ID))
    centers = filter_response(response=response, min_age=MIN_AGE)
    print(f"{datetime.utcnow()} - Centers available: {len(centers)}")
    for obj in centers:
        title = f"{obj['name']} ({obj['block_name']})"
        desc = (
            '**District: **' + obj['district'] + '\n\n' +
            '**Pincode: **' + str(obj['pincode']) + '\n\n' +
            '**Date: **' + obj['date'] + '\n\n' +
            '**Fees: **' + obj['fee_type'] + '\n\n' +
            '**Vaccine: **' + obj['vaccine'] + '\n\n' +
            '**Slots Available: **' + str(obj['available_capacity']) + '\n\n' +
            '**Link: **' + 'https://selfregistration.cowin.gov.in'
        )

        embed = discord.Embed(
            title=title,
            description=desc,
            color=discord.Color.blurple(),
            timestamp=datetime.utcnow()
        )
        embed.set_author(name='Vaccine Center for 18-44')
        await channel.send(embed=embed)


client.run(TOKEN)
