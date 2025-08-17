import discord
import os

from dotenv import load_dotenv
from transformers import pipeline

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True
client = discord.Client(intents=intents)

print("Loading Classification Model...")
classifier = pipeline("text-classification", model="ealvaradob/bert-finetuned-phishing")

@client.event
async def on_ready():
    print(f"Successfully Logged In As {client.user}")

@client.event
async def on_message(msg):
    if (msg.author != client.user):
        # print(f"Author: {msg.author}")
        # print(f"Date/Time: {msg.created_at.astimezone()}")
        # print(f"Message: {msg.content}")
        # print()
        result = classifier(msg.content)
        print(result)

client.run(TOKEN)