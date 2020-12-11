from discord.ext import commands
import asyncio, traceback, discord, inspect, textwrap, importlib, io, os, re, sys, copy, time, subprocess, platform, psutil, datetime
from contextlib import redirect_stdout
from psutil._common import bytes2human
import parsedatetime as pdt
from dateutil.relativedelta import relativedelta

# uptime

class plural:
    def __init__(self, value):
        self.value = value
    def __format__(self, format_spec):
        v = self.value
        singular, sep, plural = format_spec.partition('|')
        plural = plural or f'{singular}s'
        if abs(v) != 1:
            return f'{v} {plural}'
        return f'{v} {singular}'

def human_join(seq, delim=', ', final='or'):
    size = len(seq)
    if size == 0:
        return ''

    if size == 1:
        return seq[0]

    if size == 2:
        return f'{seq[0]} {final} {seq[1]}'

    return delim.join(seq[:-1]) + f' {final} {seq[-1]}'

def human_timedelta(dt, *, source=None, accuracy=3, brief=False, suffix=False):
    now = source or datetime.datetime.utcnow()
    # Microsecond free zone
    now = now.replace(microsecond=0)
    dt = dt.replace(microsecond=0)

    # This implementation uses relativedelta instead of the much more obvious
    # divmod approach with seconds because the seconds approach is not entirely
    # accurate once you go over 1 week in terms of accuracy since you have to
    # hardcode a month as 30 or 31 days.
    # A query like "11 months" can be interpreted as "!1 months and 6 days"
    if dt > now:
        delta = relativedelta(dt, now)
        suffix = ''
    else:
        delta = relativedelta(now, dt)
        suffix = ' ago' if suffix else ''

    attrs = [
        ('year', 'y'),
        ('month', 'mo'),
        ('day', 'd'),
        ('hour', 'h'),
        ('minute', 'm'),
        ('second', 's'),
    ]

    output = []
    for attr, brief_attr in attrs:
        elem = getattr(delta, attr + 's')
        if not elem:
            continue

        if attr == 'day':
            weeks = delta.weeks
            if weeks:
                elem -= weeks * 7
                if not brief:
                    output.append(format(plural(weeks), 'week'))
                else:
                    output.append(f'{weeks}w')

        if elem <= 0:
            continue

        if brief:
            output.append(f'{elem}{brief_attr}')
        else:
            output.append(format(plural(elem), attr))

    if accuracy is not None:
        output = output[:accuracy]

    if len(output) == 0:
        return 'now'
    else:
        if not brief:
            return human_join(output, final='and') + suffix
        else:
            return ' '.join(output) + suffix

class About (commands.Cog):
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
        embed.add_field(name=f"**Information**", value=f"**>** **Developer:** {self.bot.get_user(199375184057073664)}\n**>** **Library:** discord.py {discord.__version__}\n**>** **Python:** {platform.python_version()}\n**>** **Uptime**: {human_timedelta(self.bot.uptime)}", inline=False)
        embed.add_field(name=f"**Statistics**",  value=f"**>** **Servers:** {str(len(self.bot.guilds))}\n**>** **Users:** {len(self.bot.users)}\n**>** **Latency:** {str(int(round(self.bot.latency * 1000, 1))+ping)}ms", inline=False)
        embed.add_field(name=f"**Links**", value=f"**>** **Support Server:** SOON\n**>** **Invite:** SOON\n**>** **Vote:** SOON", inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def system(self, ctx):
        """Retrieves info about the bot's system."""
        embed = discord.Embed(title="Noxility System Information", colour=0xf2c203)
        embed.set_footer(text="Noxility", icon_url=self.bot.user.avatar_url)
        embed.add_field(name=f"**System**", value=f"**>** **Host OS:** {platform.system()}-{platform.release()}\n**>** **Uptime:** {human_timedelta(self.bot.uptime)}", inline=False)
        embed.add_field(name=f"**CPU**",  value=f"**>** **Current frequency:** {psutil.cpu_freq().current} Mhz\n**>** **Total cores:** {psutil.cpu_count()}\n**>** **Physical cores:** {psutil.cpu_count(logical=False)}\n**>** **Total Usage:** {str(psutil.cpu_percent())}%", inline=False)
        embed.add_field(name=f"**Memory**",  value=f"**>** **Total:** {bytes2human(psutil.virtual_memory().total)}\n**>** **Available:** {bytes2human(psutil.virtual_memory().available)}\n**>** **Used:** {bytes2human(psutil.virtual_memory().used)} ({psutil.virtual_memory().percent}%)", inline=False)
        embed.add_field(name=f"**Storage**",  value=f"**>** **Total:** {bytes2human(psutil.disk_usage('/').total)}\n**>** **Available:** {bytes2human(psutil.disk_usage('/').free)}\n**>** **Used:** {bytes2human(psutil.disk_usage('/').used)} ({psutil.disk_usage('/').percent}%)", inline=False)
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
    bot.add_cog(About(bot))