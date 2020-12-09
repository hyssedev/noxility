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
        ignored = (commands.CommandNotFound, commands.UserInputError)
        if isinstance(error, ignored):
            return

        if isinstance(error, commands.CommandOnCooldown):
            m, s = divmod(error.retry_after, 60)
            h, m = divmod(m, 60)
            if int(h) == 0 and int(m) == 0:
                await ctx.send(f' You need to wait {int(s)} seconds to use this command!')
            elif int(h) == 0 and int(m) != 0:
                await ctx.send(f' You need to wait {int(m)} minutes and {int(s)} seconds to use this command!')
            else:
                await ctx.send(f' You need to wait {int(h)} hours, {int(m)} minutes and {int(s)} seconds to use this command!')
        elif isinstance(error, commands.CheckFailure):
            await ctx.send("Insufficient permissions.")
        raise error

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignoring messages sent by the bot itself
        if message.author.id == self.bot.user.id:
            return

def setup(bot):
    bot.add_cog(Events(bot))