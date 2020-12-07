from discord.ext import commands
import asyncio, traceback, discord, inspect, textwrap, importlib, io, os, re, sys, copy, time, subprocess, platform, psutil, datetime
from contextlib import redirect_stdout
from psutil._common import bytes2human
import parsedatetime as pdt
from dateutil.relativedelta import relativedelta


class Misc (commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def echo(self, ctx, *, message=None):
    	message = message or "What do you want me to repeat?"
    	await ctx.message.delete()
    	await ctx.send(message)

def setup(bot):
    bot.add_cog(Misc(bot))