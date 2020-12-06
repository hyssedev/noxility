from discord.ext import commands
import asyncio, traceback, discord, inspect, textwrap, importlib, io, os, re, sys, copy, time, subprocess, platform, psutil, datetime
from contextlib import redirect_stdout
from psutil._common import bytes2human
import parsedatetime as pdt
from dateutil.relativedelta import relativedelta

class About (commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.uptime = datetime.datetime.utcnow()

    @commands.command()
    async def about(self, ctx):
        before = time.monotonic()
        await ctx.trigger_typing()
        ping = int((time.monotonic() - before) * 1000)
        embed = discord.Embed(title="Noxility", description="Noxility is a powerful bot with all kinds of commands.", colour=0xf2c203)
        embed.set_footer(text="Thank you for using Noxility!", icon_url=self.bot.user.avatar_url)
        embed.add_field(name=f"**Information**", value=f"**>** **Developer:** {self.bot.get_user(199375184057073664)}\n**>** **Library:** discord.py {discord.__version__}\n**>** **Uptime**: todo", inline=False)
        embed.add_field(name=f"**Statistics**",  value=f"**>** **Servers:** {str(len(self.bot.guilds))}\n**>** **Users:** {len(self.bot.users)}\n**>** **Latency:** {str(int(round(self.bot.latency * 1000, 1))+ping)}ms", inline=False)
        embed.add_field(name=f"**Links**", value=f"**>** **Support Server:** todo\n**>** **Invite:** todo\n**>** **Vote:** todo", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def system(self, ctx):
        embed = discord.Embed(title="Noxility System Information", colour=0xf2c203)
        embed.set_footer(text="Noxility", icon_url=self.bot.user.avatar_url)
        embed.add_field(name=f"**System**", value=f"**>** **Host OS:** {platform.system()}-{platform.release()}\n**>** **Uptime:** todo", inline=False)
        embed.add_field(name=f"**CPU**",  value=f"**>** **Current frequency:** {psutil.cpu_freq().current} Mhz\n**>** **Total cores:** {psutil.cpu_count()}\n**>** **Physical cores:** {psutil.cpu_count(logical=False)}\n**>** **Total Usage:** {str(psutil.cpu_percent())}%", inline=False)
        embed.add_field(name=f"**Memory**",  value=f"**>** **Total:** {bytes2human(psutil.virtual_memory().total)}\n**>** **Available:** {bytes2human(psutil.virtual_memory().available)}\n**>** **Used:** {bytes2human(psutil.virtual_memory().used)} ({psutil.virtual_memory().percent}%)", inline=False)
        embed.add_field(name=f"**Storage**",  value=f"**>** **Total:** {bytes2human(psutil.disk_usage('/').total)}\n**>** **Available:** {bytes2human(psutil.disk_usage('/').free)}\n**>** **Used:** {bytes2human(psutil.disk_usage('/').used)} ({psutil.disk_usage('/').percent}%)", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    async def guildbanner(self, ctx):
        if not ctx.guild.icon: return await ctx.send("This server does not have a banner.")
        embed = discord.Embed(title=f"{ctx.guild.name}'s banner", color=0xf2c203, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.set_image(url=f'{ctx.guild.banner_url}')
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(About(bot))