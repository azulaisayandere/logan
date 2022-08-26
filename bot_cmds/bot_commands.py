from asyncio import sleep
from datetime import datetime
from discord import Forbidden, File, Intents
from discord.ext import commands
from logs.logs import masslist
from pandas import DataFrame

# Establish client user
intents = Intents.all()
client = commands.Bot(command_prefix="logan ", intents=intents)

# i hate rewriting this every time
async def typing(ctx, x):
    await ctx.channel.typing()
    await sleep(x)

# role ids for debugging
test = 1010746100958900284
vrcc = 793013468256010270

# Discord commands
@client.command()
@commands.has_role(test) # put in json file for easier appending later on
async def export(ctx):
    for guilds in masslist:
        if guilds['guid'] == ctx.guild.id:
            DataFrame(guilds['users'], columns=['name', 'cnt']).to_csv(f'{ctx.guild.id}_user_log.csv') # export by server via command
            await typing(ctx, 3)
            await ctx.send(file=File(f'{ctx.guild.id}_user_log.csv'))
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Exported message count log for {ctx.guild}!")

@client.command()
async def stats(ctx, name):
    for guilds in masslist:
        if guilds['guid'] == ctx.guild.id:
            try:
                for user in guilds['users']:
                    if name == "me":
                        if ctx.author.id == user['uid']:
                            await typing(ctx, 2)
                            await ctx.channel.send(f"logan Stats for {user['name']}, Message Count: {user['cnt']}")
                    else:
                        if (name == user['name']) or (name == f"<@{user['uid']}>"):
                            await typing(ctx, 2)
                            await ctx.channel.send(f"logan Stats for {user['name']}, Message Count: {user['cnt']}")
            except Forbidden:
                print(f"[{ctx.message.created_at.strftime('%H:%M:%S')}] Forbidden 403 Encountered")

@client.event
async def on_command_error(ctx, error):
    if repr(error).startswith("MissingRequiredArgument"):
        try:
            await typing(ctx, 2)
            await ctx.channel.send("Missing argument(s)")
        except Forbidden:
            print(f"[{ctx.message.created_at.strftime('%H:%M:%S')}] Forbidden 403 Encountered")