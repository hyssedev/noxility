from discord.ext import commands
import asyncio, traceback, discord, inspect, textwrap, importlib, io, os, re, sys, copy, time, subprocess, platform, psutil, datetime
from contextlib import redirect_stdout
from psutil._common import bytes2human
import parsedatetime as pdt
from dateutil.relativedelta import relativedelta
from discord.ext import commands

class Misc (commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    

def setup(bot):
    bot.add_cog(Misc(bot))