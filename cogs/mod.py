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
    @commands.bot_has_permissions(kick_members=True)
    @commands.has_guild_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """Kicks specified member."""
        # if member is None: return await ctx.send("Error, invalid member.")
        if await cogs._utils.role_hierarchy(ctx, member): return
        if ctx.guild.me.top_role <= member.top_role:
            return await ctx.send(f"Error, you can't do this because my role is lower than **{member.name}**.")
        await ctx.guild.kick(discord.Object(id=member.id), reason=reason)
        await ctx.send(f"✅ Successfully **{str(ctx.command.name)}ed** {member.name}.")

def setup(bot):
    bot.add_cog(Mod(bot))