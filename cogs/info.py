from discord.ext import commands
import asyncio, traceback, discord, inspect, textwrap, importlib, io, os, re, sys, copy, time, subprocess, platform, psutil, datetime
from contextlib import redirect_stdout
from psutil._common import bytes2human
import parsedatetime as pdt
from dateutil.relativedelta import relativedelta
from cogs._utils import human_timedelta

emote = "<:noxilityarrow:786985788893560923>"

class Info (commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.uptime = datetime.datetime.utcnow()

    @commands.command(aliases=["info"])
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def about(self, ctx):
        """Retrieves info about the bot."""
        before = time.monotonic()
        await ctx.trigger_typing()
        ping = int((time.monotonic() - before) * 1000)
        embed = discord.Embed(title="Noxility", description="Noxility is a powerful bot with all kinds of commands.", colour=0xf2c203)
        embed.set_footer(text="Thank you for using Noxility!", icon_url=self.bot.user.avatar_url)
        embed.add_field(name=f"**General Information**", value=f"{emote} **Developer:** {self.bot.get_user(199375184057073664)}\n{emote} **Library:** discord.py {discord.__version__}\n{emote} **Uptime**: {human_timedelta(self.bot.uptime)}\n{emote} **Created**: 6 December 2020 ({human_timedelta(datetime.datetime(2020, 12, 6))} ago)\n{emote} **Python:** {platform.python_version()}", inline=False)
        embed.add_field(name=f"**Stats**",  value=f"{emote} **Commands loaded:** {len(self.bot.commands)}\n{emote} **Servers:** {str(len(self.bot.guilds))}\n{emote} **Users:** {len(self.bot.users)}\n{emote} **Latency:** {str(int(round(self.bot.latency * 1000, 1))+ping)}ms", inline=False)
        embed.add_field(name=f"**Links**", value=f"{emote} **Support Server:** [Noxility](https://discord.gg/hHnejD2Xd6)\n{emote} **Invite:** SOON\n{emote} **Vote:** SOON", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def system(self, ctx):
        """Retrieves info about the bot's system."""
        embed = discord.Embed(title="Noxility System Information", colour=0xf2c203)
        embed.set_footer(text="Noxility", icon_url=self.bot.user.avatar_url)
        embed.add_field(name=f"**System**", value=f"{emote} **Host OS:** {platform.system()}-{platform.release()}\n{emote} **Uptime:** {human_timedelta(datetime.datetime.fromtimestamp(psutil.boot_time()))}", inline=False)
        embed.add_field(name=f"**CPU**",  value=f"{emote} **Current frequency:** {psutil.cpu_freq().current} Mhz\n{emote} **Total cores:** {psutil.cpu_count()}\n{emote} **Physical cores:** {psutil.cpu_count(logical=False)}\n{emote} **Total Usage:** {str(psutil.cpu_percent())}%", inline=False)
        embed.add_field(name=f"**Memory**",  value=f"{emote} **Total:** {bytes2human(psutil.virtual_memory().total)}\n{emote} **Available:** {bytes2human(psutil.virtual_memory().available)}\n{emote} **Used:** {bytes2human(psutil.virtual_memory().used)} ({psutil.virtual_memory().percent}%)", inline=False)
        embed.add_field(name=f"**Storage**",  value=f"{emote} **Total:** {bytes2human(psutil.disk_usage('/').total)}\n{emote} **Available:** {bytes2human(psutil.disk_usage('/').free)}\n{emote} **Used:** {bytes2human(psutil.disk_usage('/').used)} ({psutil.disk_usage('/').percent}%)", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def guildbanner(self, ctx):
        """Retrieves the current guild's banner"""
        if not ctx.guild.icon: return await ctx.send("This server does not have a banner.")
        embed = discord.Embed(title=f"{ctx.guild.name}'s banner", color=0xf2c203, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.set_image(url=f'{ctx.guild.banner_url}')
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Info(bot))