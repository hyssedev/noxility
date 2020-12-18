from discord.ext import commands
import discord, os, asyncio, logging
import cogs._utils

bot = commands.Bot(command_prefix=['nox ', 'Nox ', 'NOX ', 'noxility', 'Noxility'], owner_id=199375184057073664, intents=discord.Intents.all(), help_command=cogs._utils.EmbedHelpCommand(), description="Noxility is a powerful bot with all kinds of commands, ready to make your server more fun & enjoyable.")
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

bot.run("Nzg1MTI4MjI4MjEyNzAzMjMz.X8zVpA.uPGZzBpz1sW6LXEtUoPzW8W52zo")