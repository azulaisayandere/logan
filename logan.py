# shoutouts to stackoverflow

from bot_cmds.bot_commands import client
from config import LOGAN
from datetime import datetime
from discord import Game
from logs.logs import log_data
from sys import version

# print version
print(f"[{datetime.now().strftime('%H:%M:%S')}] running Python {version}")

# other Discord interactions and funnies
@client.event
async def on_ready():
    await client.change_presence(activity=Game(name="the number counting game"))
    print(f"[{datetime.now().strftime('%H:%M:%S')}] fired up on {client.user}!")

@client.event
async def on_message(message):
    if message.author != client.user:
        await log_data(message)

    await client.process_commands(message)

client.run(LOGAN)