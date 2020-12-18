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

    @commands.command(enabled=False)
    @commands.guild_only()
    @commands.bot_has_permissions(kick_members=True)
    @commands.has_guild_permissions(kick_members=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """Kicks specified member."""
        if await cogs._utils.role_hierarchy(ctx, member): return
        if ctx.guild.me.top_role <= member.top_role:
            return await ctx.send(f"Error, you can't do this because my role is lower than **{member.name}**.")
        await ctx.guild.kick(discord.Object(id=member.id), reason=reason)
        await ctx.send(f"✅ Successfully **{str(ctx.command.name)}ed** {member.name}.")

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(manage_messages=True)
    @commands.has_permissions(manage_messages=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def purge(self, ctx, amount: str):
        """Purge an amount of messages in a channel."""
        if not amount.isnumeric(): return await ctx.send("Error, please enter a correct number.")
        if int(amount)>500 or int(amount)<1:
            return await ctx.send('Error, invalid amount. Please enter a number between 2 and 500.')
        await ctx.message.delete()
        await ctx.message.channel.purge(limit=int(amount))
        await ctx.send(f"✅ Sucesfully deleted **{int(amount)}** message{cogs._utils.plural_check(int(amount))}!", delete_after=5)

    @commands.command(enabled=False, hidden=True)
    @commands.guild_only()
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ban(self, ctx, user: discord.User):
        if await cogs._utils.role_hierarchy(ctx, user): return
        try:
            await ctx.guild.ban(discord.Object(id=user.id))
        except:
            return await ctx.send(f"Error, can't ban member {user.name}.")



def setup(bot):
    bot.add_cog(Mod(bot))