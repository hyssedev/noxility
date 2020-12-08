from discord.ext import commands
import discord, os, asyncio, logging
import cogs._utils

bot = commands.Bot(command_prefix=['nox ', 'Nox ', 'NOX '], owner_id=199375184057073664, intents=discord.Intents.all())
bot.remove_command("help")
logging.basicConfig(level=logging.INFO) 

for cog in os.listdir("cogs"):
    if cog.endswith(".py") and not cog.startswith("_"):
        try:
            cog = f"cogs.{cog.replace('.py', '')}"
            bot.load_extension(cog)
            print(f"{cog} loaded.")
        except Exception as e:
            print(f"{cog} couldn't be loaded.")
            raise e        

"""
# advanced logging system
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)
"""

bot.run("Nzg1MTI4MjI4MjEyNzAzMjMz.X8zVpA.uPGZzBpz1sW6LXEtUoPzW8W52zo")