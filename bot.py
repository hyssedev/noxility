from discord.ext import commands
import discord, os, asyncio, logging, dbl
import utils.utils
from . import secret

bot = commands.AutoShardedBot(command_prefix=['nox ', 'Nox ', 'NOX ', 'noxility', 'Noxility'], owner_id=199375184057073664, intents=discord.Intents.all(), help_command=utils.utils.EmbedHelpCommand(), description="Noxility is a powerful bot with all kinds of commands, ready to make your server more fun & enjoyable.", shard_count=2)
logging.basicConfig(level=logging.INFO) 

# top gg stuff
token = secret.token  # set this to your DBL token
bot.dblpy = dbl.DBLClient(bot, token, webhook_path='/dblwebhook', webhook_auth=secret.webhook_auth, webhook_port=5000, autopost=True)
bot.usage = {}

for cog in os.listdir("cogs"):
    if cog.endswith(".py") and not cog.startswith("_"):
        try:
            cog = f"cogs.{cog.replace('.py', '')}"
            bot.load_extension(cog)
            print(f"{cog} loaded.")
        except Exception as e:
            print(f"{cog} couldn't be loaded.")
            raise e      

bot.run(secret.bot_token)