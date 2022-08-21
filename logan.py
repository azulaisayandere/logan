# shoutouts to stackoverflow and charles from which i stole the basis for a lot of this code
# objectives: + done * in progress x not started
# spam every nth message [+]
# target specific users [+]
# log user data [+]
# log frequency data[+], most active users[+], message times [+] 
# move logs from json to mariadb [x]
# pedophile slaughterhouse contribution [+] now removed, 37,846 kid diddlers dead :)
# train language model [x]

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