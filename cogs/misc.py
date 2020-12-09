from discord.ext import commands
import asyncio, traceback, discord, inspect, textwrap, importlib, io, os, re, sys, copy, time, subprocess, platform, psutil
from contextlib import redirect_stdout
from psutil._common import bytes2human
import parsedatetime as pdt
from dateutil.relativedelta import relativedelta
from datetime import datetime

class Misc (commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def channelinfo(self, ctx):
        embed = discord.Embed(title=f"Stats for **{ctx.channel.name}**", description=f"Category: {ctx.channel.category.name if ctx.channel.category else 'No category'}", color=0xf2c203)
        embed.add_field(name="Guild", value=ctx.guild.name, inline=False)
        embed.add_field(name="ID", value=ctx.channel.id, inline=False)
        embed.add_field(name="Topic", value=f"{ctx.channel.topic if ctx.channel.topic else 'No topic.'}", inline=False)
        embed.add_field(name="Position", value=ctx.channel.position, inline=False)
        embed.add_field(name="Slowmode Delay", value=ctx.channel.slowmode_delay, inline=False)
        embed.add_field(name="NSFW", value=ctx.channel.is_nsfw(), inline=False)
        embed.add_field(name="NEWS", value=ctx.channel.is_news(), inline=False)
        embed.add_field(name="Creation Time", value=ctx.channel.created_at.strftime("%d %B, %Y"), inline=False)
        embed.add_field(name="Permissions Synced", value=ctx.channel.permissions_synced, inline=False)
        embed.add_field(name="Hash", value=hash(ctx.channel), inline=False)

        await ctx.send(embed=embed)
    

def setup(bot):
    bot.add_cog(Misc(bot))