from asyncio import sleep
from datetime import datetime
from discord import Forbidden, File
from discord.ext import commands
from logs.logs import masslist
from pandas import DataFrame

# Establish client user
client = commands.Bot(command_prefix="logan ")

# i hate rewriting this every time
async def typing(ctx, x):
    await ctx.channel.trigger_typing()
    await sleep(x)

# Discord commands
@client.command()
async def export(ctx):
    if ctx.author.id == 204366690446737419:
        for guilds in masslist:
            if guilds['guid'] == ctx.guild.id:
                df = DataFrame(guilds['users'], columns=['name', 'cnt'])
                df.to_csv(f'{ctx.guild.id}_user_log.csv') # export by server via command
                await typing(ctx, 3)
                await ctx.send(file=File(f'{ctx.guild.id}_user_log.csv'))
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Exported message count log for {ctx.guild}!")
        try:
            await typing(ctx, 1)
            await ctx.channel.send("you're not my master fuck off")
        except Forbidden:
            print(f"[{ctx.message.created_at.strftime('%H:%M:%S')}] Forbidden 403 Encountered")

# @client.event
# async def on_command_error(ctx, error):
#     if repr(error).startswith("MissingRequiredArgument"):
#         try:
#             await typing(ctx, 2)
#             await ctx.channel.send("Missing argument(s)")
#         except Forbidden:
#             print(f"[{ctx.message.created_at.strftime('%H:%M:%S')}] Forbidden 403 Encountered")