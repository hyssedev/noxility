from discord.ext import commands
import asyncio, traceback, discord, inspect, textwrap, importlib, io, os, re, sys, copy, time, subprocess, platform, psutil
from contextlib import redirect_stdout
from psutil._common import bytes2human
import parsedatetime as pdt
from dateutil.relativedelta import relativedelta
from datetime import datetime
import cogs._utils
from cogs._utils import emote

class Misc (commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    async def lines(self, ctx):
        """Shows how many lines the Noxility project currently has."""
        embed = discord.Embed(colour=0xf2c203)
        embed.add_field(name="This project currently has", value=f"{cogs._utils.countlines(r'/root/noxility/')} lines")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Misc(bot))