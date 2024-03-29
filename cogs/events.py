#pylint: disable=E0401
import asyncio, traceback, discord, inspect, textwrap, importlib, io, os, re, sys, copy, time, subprocess, platform, psutil, datetime, json, dbl
from contextlib import redirect_stdout
from psutil._common import bytes2human
import parsedatetime as pdt
from dateutil.relativedelta import relativedelta
from discord.ext import commands
import utils.utils

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
            if int(h) == 0 and int(m) == 0:
                await ctx.send(f" You need to wait {int(s) if s > 1 else round(s, 1)} second{'s' if int(s) != 1 else ''} to use this command!", delete_after=5)
            elif int(h) == 0 and int(m) != 0:
                await ctx.send(f" You need to wait {int(m)} minute{'s' if int(m) != 1 else ''} and {int(s)} second{'s' if int(s) != 1 else ''} to use this command!", delete_after=5)
            else:
                await ctx.send(f" You need to wait {int(h)} hour{'s' if int(h) != 1 else ''}, {int(m)} minute{'s' if int(m) != 1 else ''} and {int(s)} second{'s' if int(s) != 1 else ''} to use this command!", delete_after=5)
        elif isinstance(error, commands.MaxConcurrencyReached):
            await ctx.send("Error, you've reached max capacity of command usage at once, please finish the previous one.", delete_after=5)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"Error, `{error.param.name}` is a required argument that is missing.", delete_after=5)
        elif isinstance(error, commands.MemberNotFound):
            await ctx.send(f"Error, I couldn't find specified member.", delete_after=5)
        elif isinstance(error, commands.UserNotFound):
            await ctx.send(f"Error, I couldn't find specified user.", delete_after=5)
        elif isinstance(error, commands.RoleNotFound):
            await ctx.send(f"Error, I couldn't find specified role.", delete_after=5)
        elif isinstance(error, commands.EmojiNotFound):
            await ctx.send(f"Error, I couldn't find specified emoji.", delete_after=5)
        elif isinstance(error, commands.DisabledCommand):
            await ctx.send(f'{ctx.command} has been disabled temporarily.', delete_after=5)
        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(f'{ctx.command} can not be used in Private Messages.', delete_after=5)
            except discord.HTTPException:
                pass

        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("Error, you have insufficient permissions.", delete_after=5)
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send("Error, I do not have required permissions to do this.", delete_after=5)
        else:
            # All other Errors not returned come here. And we can just print the default TraceBack.
            await ctx.send("Unknown error occured, if you think this is a mistake please report it in our Support Server. Use `nox support` to see it.", delete_after=5)
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
            
        elif isinstance(error, commands.BadArgument):
            await ctx.send("Seems like you're giving me a bad argument.")
        elif isinstance(error, commands.TooManyArguments):
            await ctx.send("Error, you're giving me too many arguments.")
        """

    @commands.Cog.listener()
    async def on_command(self, ctx):
        try:
            self.bot.usage[ctx.command.qualified_name] += 1
        except KeyError:
            self.bot.usage[ctx.command.qualified_name] = 1

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignoring messages sent by the bot itself
        if message.author.id == self.bot.user.id:
            return

    # ----- top.gg server count auto -----
    @commands.Cog.listener()
    async def on_guild_post(self):
        print("Server count posted successfully")

    # ------ top.gg vote counter auto ------
    @commands.Cog.listener()
    async def on_dbl_vote(self, data):
        channel = self.bot.get_channel(791284042732666891)
        user = self.bot.get_user(int(data['user']))
        embed = discord.Embed(colour=0xf2c203, description=f"**{user}** has just voted for **Noxility**, you can vote for the bot [here](https://top.gg/bot/785128228212703233/vote).")
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_dbl_test(self, data):
        channel = self.bot.get_channel(791284042732666891)
        user = self.bot.get_user(int(data['user']))
        embed = discord.Embed(colour=0xf2c203, description=f"**{user}** has just voted for **Noxility**, you can vote for the bot [here](https://top.gg/bot/785128228212703233/vote).")
        await channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Events(bot))