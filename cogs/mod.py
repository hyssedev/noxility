#pylint: disable=E0401
from discord.ext import commands
import asyncio, traceback, discord, inspect, textwrap, importlib, io, os, re, sys, copy, time, subprocess, platform, psutil
from contextlib import redirect_stdout
from psutil._common import bytes2human
import parsedatetime as pdt
from dateutil.relativedelta import relativedelta
from datetime import datetime
import utils.utils

class Mod (commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(kick_members=True)
    @commands.has_guild_permissions(kick_members=True)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """Kicks specified member."""
        if ctx.guild.me.top_role <= member.top_role: return await ctx.send(f"Error, you can't do this because my role is lower than **{member.name}**.")
        if ctx.author.id != ctx.guild.owner.id:
            if ctx.author.top_role <= member.top_role: return await ctx.send(f"Error, you can't do this because **{member.name}** has a higher role than you do.")
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
        await ctx.send(f"✅ Sucesfully deleted **{int(amount)}** message{utils.utils.plural_check(int(amount))}!", delete_after=5)
    
    """
    # disabled, this command does not support banning people that are not in the current guild
    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ban(self, ctx, member: discord.Member):
        Bans specified user, currently only works on members that are on the current server.
        if ctx.guild.me.top_role <= member.top_role: return await ctx.send(f"Error, you can't do this because my role is lower than **{member.name}**.")
        if ctx.author.id != ctx.guild.owner.id:
            if ctx.author.top_role <= member.top_role: return await ctx.send(f"Error, you can't do this because **{member.name}** has a higher role than you do.")
        try:
            await ctx.guild.ban(discord.Object(id=member.id))
            await ctx.send(f"✅ Sucesfully banned **{member.name}#{member.discriminator}**!")
        except:
            return await ctx.send(f"Error, can't ban member {member.name}.")
    """

    @commands.command()
    @commands.guild_only()
    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ban(self, ctx, member: utils.utils.MemberID):
        """Bans specified user. Works even if the member is not in the current guild."""
        try:
            if ctx.author.id != ctx.guild.owner.id:
                if ctx.author.top_role <= member.top_role: return await ctx.send(f"Error, you can't do this because **{member.name}** has a higher role than you do.")
        except:
            pass
        await ctx.guild.ban(member)
        await ctx.send(f"✅ Sucesfully banned **{member}**!")

def setup(bot):
    bot.add_cog(Mod(bot))