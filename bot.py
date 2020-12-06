from discord.ext import commands
import discord, os, asyncio, logging

intents = discord.Intents.all()

bot = commands.Bot(command_prefix=commands.when_mentioned_or('nox '), intents=intents)

bot.remove_command("help")

for cog in os.listdir("cogs"):
    if cog.endswith(".py"):
        if cog != "__init__.py":
            try:
                cog = f"cogs.{cog.replace('.py', '')}"
                bot.load_extension(cog)
                print(f"{cog} loaded.")
            except Exception as e:
                print(f"{cog} couldn't be loaded.")
                raise e        

@bot.command()
@commands.is_owner()
async def reload(ctx, cog=None):
    """
    Usage: <prefix> reload <cog>
    It reloads a cog. You can use this if a cog is not working correctly.
    """
    cogs = []
    for cogg in os.listdir("cogs"):
        if cogg.endswith(".py"):
            if cogg != "__init__.py":
                cogs.append(cogg)
    if cog is None: await ctx.send(f"Please specify which cog to reload. Available cogs: {cogs}.")
    else:
        try:
            bot.unload_extension(f"cogs.{cog}")
            bot.load_extension(f"cogs.{cog}")
            await ctx.send(f"Successfully reloaded {cog}.")
            print(f"Reloaded{cog}.")
        except Exception as e:
            await ctx.send(f"I couldn't reload {cog}.")
            print(f"{cog} couldn't be reloaded.")
            raise e

"""
# logging system
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
"""

bot.run("")