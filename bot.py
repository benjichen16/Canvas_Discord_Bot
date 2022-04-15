import discord
from dotenv import load_dotenv
import os
import canvas_api

load_dotenv()

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        assignments = canvas_api.Canvas(os.getenv("CANVAS_ACCESS_TOKEN")).get_assignments()
        await message.channel.send(assignments)

client.run(os.getenv('TOKEN'))
