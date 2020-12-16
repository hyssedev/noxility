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
    async def rolemembers(self, ctx, role: discord.Role):
        """Shows how many members have the specified role."""
        start = time.time()
        pages = []
        count = 1
        for i in range(0, len(role.members), 15):
            members = ""
            next_members = role.members[i : i + 15]
            for member in next_members:
                members += f"`[{count}]` **{member}** (ID: {member.id})\n"
                count += 1
            pages.append(members)
        pages2 = [s + f"\n`{len(pages)} page{'s' if len(pages) > 1 else ''}, {count-1} {'entries' if count-1 > 1 else 'entry'}`" for s in pages]
        end = time.time()
        print(f"Calculations took {end - start} seconds.")
        await cogs._utils.Pag(color=0xf2c203, entries=pages2, length=1, timeout=30).start(ctx)

def setup(bot):
    bot.add_cog(Misc(bot))