from discord.ext import commands
import asyncio, traceback, discord, inspect, textwrap, importlib, io, os, re, sys, copy, time, subprocess, platform, psutil
from contextlib import redirect_stdout
from psutil._common import bytes2human
import parsedatetime as pdt
from dateutil.relativedelta import relativedelta
from datetime import datetime
import cogs._utils

class Mod (commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(kick_members=True)
    async def kick(self, ctx, member: cogs._utils.MemberID, *, reason=None):
        if await cogs._utils.role_hierarchy(ctx, member): return
        await ctx.guild.kick(discord.Object(id=member.id))
        embed = discord.Embed(title=f"{member.name} got kicked by Similarty", description=reason, color=0xf2c203)
        await ctx.send(embed=embed)
    

def setup(bot):
    bot.add_cog(Mod(bot))