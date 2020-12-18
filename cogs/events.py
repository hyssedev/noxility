import asyncio, traceback, discord, inspect, textwrap, importlib, io, os, re, sys, copy, time, subprocess, platform, psutil, datetime, json
from contextlib import redirect_stdout
from psutil._common import bytes2human
import parsedatetime as pdt
from dateutil.relativedelta import relativedelta
from discord.ext import commands
import cogs._utils

class Events (commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"-----Logged in as {self.bot.user.name}.-----")
        # moved to a task to do this every hour
        # await self.bot.change_presence(activity=discord.Game(name=f"nox help | {str(len(self.bot.guilds))} servers"))

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        # Ignoring CommandNotFound and UserInputError
        ignored = (commands.CommandNotFound, commands.NotOwner)
        if isinstance(error, ignored):
            return

        error = getattr(error, 'original', error)
        if isinstance(error, commands.CommandOnCooldown):
            m, s = divmod(error.retry_after, 60)
            h, m = divmod(m, 60)
            seconds = int(s) if s > 1 else round(s, 1)
            if int(h) == 0 and int(m) == 0:
                message = await ctx.send(f" You need to wait {int(s) if s > 1 else round(s, 1)} second{'s' if int(s) != 1 else ''} to use this command!")
            elif int(h) == 0 and int(m) != 0:
                message = await ctx.send(f" You need to wait {int(m)} minute{'s' if int(m) != 1 else ''} and {int(s)} second{'s' if int(s) != 1 else ''} to use this command!")
            else:
                message = await ctx.send(f" You need to wait {int(h)} hour{'s' if int(h) != 1 else ''}, {int(m)} minute{'s' if int(m) != 1 else ''} and {int(s)} second{'s' if int(s) != 1 else ''} to use this command!")
            await asyncio.sleep(5)
            await message.delete()
        elif isinstance(error, commands.MaxConcurrencyReached):
            message = await ctx.send("Error, you've reached max capacity of command usage at once, please finish the previous one.")
            await asyncio.sleep(5)
            await message.delete()
        elif isinstance(error, commands.MissingRequiredArgument):
            message = await ctx.send(f"Error, `{error.param.name}` is a required argument that is missing.")
            await asyncio.sleep(5)
            await message.delete()
        elif isinstance(error, commands.MemberNotFound):
            message = await ctx.send(f"Error, I couldn't find specified member.")
            await asyncio.sleep(5)
            await message.delete()
        elif isinstance(error, commands.RoleNotFound):
            message = await ctx.send(f"Error, I couldn't find specified role.")
            await asyncio.sleep(5)
            await message.delete()
        elif isinstance(error, commands.EmojiNotFound):
            message = await ctx.send(f"Error, I couldn't find specified emoji.")
            await asyncio.sleep(5)
            await message.delete()
        elif isinstance(error, commands.DisabledCommand):
            message = await ctx.send(f'{ctx.command} has been disabled temporarily.')
            await asyncio.sleep(5)
            await message.delete()
        elif isinstance(error, commands.NoPrivateMessage):
            try:
                message = await ctx.author.send(f'{ctx.command} can not be used in Private Messages.')
                await asyncio.sleep(5)
                await message.delete()
            except discord.HTTPException:
                pass

        elif isinstance(error, commands.MissingPermissions):
            message = await ctx.send("Error, you have insufficient permissions.")
            await asyncio.sleep(5)
            await message.delete()
        elif isinstance(error, commands.BotMissingPermissions):
            message = await ctx.send("Error, I do not have required permissions to do this.")
            await asyncio.sleep(5)
            await message.delete()
        else:
            # All other Errors not returned come here. And we can just print the default TraceBack.
            message = await ctx.send("Unknown error occured, if you think this is a mistake please report it in our Support Server. Use `nox support` to see it.")
            await asyncio.sleep(5)
            await message.delete()
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)
        """ 
        # For this error example we check to see where it came from...
        elif isinstance(error, commands.BadArgument):
            if ctx.command.qualified_name == 'tag list':  # Check if the command being invoked is 'tag list'
                await ctx.send('I could not find that member. Please try again.')
            elif ctx.command.qualified_name == 'kick':
                await ctx.send('I could not find that member. Please try again.')
        # check failure contains missing permissions and bot missing permissions
        elif isinstance(error, commands.CheckFailure):
            await ctx.send("Insufficient permissions.")

        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("Error, missing permissions.")
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send("Error, I do not have required permissions to do this.")
            
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Seems like you're giving me a bad argument.")
        elif isinstance(error, commands.TooManyArguments):
            await ctx.send("Error, you're giving me too many arguments.")

        """

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignoring messages sent by the bot itself
        if message.author.id == self.bot.user.id:
            return

def setup(bot):
    bot.add_cog(Events(bot))