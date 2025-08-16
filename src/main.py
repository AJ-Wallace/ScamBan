import discord
import os

from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CHANNEL_NAME = os.getenv('CHANNEL_NAME')

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    for guild in client.guilds:
        if guild.name == GUILD:
            break

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )
    
    channel = discord.utils.get(guild.text_channels, name=CHANNEL_NAME)
    if channel is None:
        print(f"Channel '{CHANNEL_NAME}' not found")
        return

    # Send the message
    await channel.send("Hello, this is a test message!")

client.run(TOKEN)