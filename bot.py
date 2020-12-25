from discord.ext import commands
import discord, os, asyncio, logging, dbl
import utils.utils

bot = commands.AutoShardedBot(command_prefix=['nox ', 'Nox ', 'NOX ', 'noxility', 'Noxility'], owner_id=199375184057073664, intents=discord.Intents.all(), help_command=utils.utils.EmbedHelpCommand(), description="Noxility is a powerful bot with all kinds of commands, ready to make your server more fun & enjoyable.", shard_count=2)
logging.basicConfig(level=logging.INFO) 

# top gg stuff
token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6Ijc4NTEyODIyODIxMjcwMzIzMyIsImJvdCI6dHJ1ZSwiaWF0IjoxNjA4NzI1Mjg0fQ.IdeT0YpZOGa-fch94gGFPwcnQgIK1uBvp2sxAlrsbmI'  # set this to your DBL token
bot.dblpy = dbl.DBLClient(bot, token, webhook_path='/dblwebhook', webhook_auth='=nSebdFy$x?AAshZ!VaX8a$fj', webhook_port=5000, autopost=True)

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