#pylint: disable=E0401
from discord.ext import commands
import asyncio, traceback, discord, inspect, textwrap, importlib, io, os, re, sys, copy, time, subprocess, platform, psutil, datetime
from contextlib import redirect_stdout
from psutil._common import bytes2human
import parsedatetime as pdt
from dateutil.relativedelta import relativedelta

from utils.utils import human_timedelta
import utils.utils
from utils.utils import emote

class Bot_Info (commands.Cog):
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
        counter = 0
        for i in self.bot.guilds:
            for j in i.channels:
                counter += 1
        embed = discord.Embed(title="Noxility", description="Noxility is a powerful bot with all kinds of commands.", colour=0xf2c203)
        embed.set_footer(text="Thank you for using Noxility!", icon_url=self.bot.user.avatar_url)
        embed.add_field(name=f"**General Information**", value=f"{emote} **Developer:** {self.bot.get_user(199375184057073664)}\n{emote} **Library:** discord.py {discord.__version__}\n{emote} **Uptime**: {human_timedelta(self.bot.uptime)}\n{emote} **Created**: 6 December 2020 ({human_timedelta(datetime.datetime(2020, 12, 6))} ago)\n{emote} **Python:** {platform.python_version()}", inline=False)
        embed.add_field(name=f"**Stats**",  value=f"{emote} **Commands loaded:** {len([i for i in self.bot.walk_commands()])}\n{emote} **Cogs:** {len(self.bot.cogs)}\n{emote} **Servers:** {str(len(self.bot.guilds))}\n{emote} **Channels:** {counter}\n{emote} **Users:** {len(self.bot.users)}\n{emote} **Latency:** Websocket: {int(round(self.bot.latency * 1000, 1))}ms, Message: {ping}ms", inline=False)
        embed.add_field(name=f"**Links**", value=f"{emote} **Support Server:** [Noxility](https://discord.gg/BnzYDcKWbt)\n{emote} **Invite:** [click here](https://discord.com/api/oauth2/authorize?client_id=785128228212703233&permissions=8&scope=bot)\n{emote} **Vote:** [click here](https://top.gg/bot/785128228212703233/vote)", inline=False)
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
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def support(self, ctx):
        """Shows Noxility's Server invite link."""
        try:
            # try sending a dm
            user = self.bot.get_user(ctx.author.id)
            await user.send(f"{emote} **Noxility Server** - https://discord.gg/BnzYDcKWbt")
            await ctx.send("Sent you a DM with the Support Server invite link.")
        except:
            # if author has server messages disabled, send message to that channel
            await ctx.send(f"{emote} **Noxility Server** - https://discord.gg/BnzYDcKWbt")

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def invite(self, ctx):
        """Shows Noxility's invite link."""
        try:
            # try sending a dm
            user = self.bot.get_user(ctx.author.id)
            await user.send(f"{emote} **Noxility Invite Link** - https://discord.com/api/oauth2/authorize?client_id=785128228212703233&permissions=8&scope=bot")
            await ctx.send("Sent you a DM with Noxility's invite link.")
        except:
            # if author has server messages disabled, send message to that channel
            await ctx.send(f"{emote} **Noxility Invite Link** - https://discord.com/api/oauth2/authorize?client_id=785128228212703233&permissions=8&scope=bot")

    @commands.command()
    @commands.cooldown(1, 60*60*6, commands.BucketType.user)
    async def feedback(self, ctx, *, text: str):
        """Sends any kind of feedback to the developers: bugs, suggestions and so on."""
        channel = self.bot.get_channel(787694632074608640)
        created = (ctx.message.created_at).strftime("%d %B, %Y, %H:%M")
        await channel.send(f"**Feedback from {ctx.author.name}#{ctx.author.discriminator} (ID: {ctx.author.id})**\n{emote} Text: {text}\n\n{emote} Feedback sent on **{created}**.")
        await ctx.send("Thank you for your feedback.")

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def ping(self, ctx):
        """Shows the bot websocket & message sending latency."""
        before = time.monotonic()
        await ctx.trigger_typing()
        ping = int((time.monotonic() - before) * 1000)
        wsping = round(self.bot.latency*1000)
        embed = discord.Embed(title="Latency", description=f"**Message latency:** `{ping}ms`\n**Websocket latency:** `{wsping}ms`", colour=0xf2c203)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    async def lines(self, ctx):
        """Shows how many lines the Noxility project currently has."""
        embed = discord.Embed(colour=0xf2c203)
        embed.add_field(name="This project currently has", value=f"{utils.utils.countlines(r'/root/noxility/')} lines")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def vote(self, ctx):
        """Shows Noxility's vote link."""
        try:
            # try sending a dm
            user = self.bot.get_user(ctx.author.id)
            await user.send(f"{emote} **Noxility Vote Link** - https://top.gg/bot/785128228212703233/vote\n\nThank you for voting me!")
            await ctx.send("Sent you a DM with Noxility's vote link.")
        except:
            # if author has server messages disabled, send message to that channel
            await ctx.send(f"{emote} **Noxility Vote Link** - https://top.gg/bot/785128228212703233/vote\n\nThank you for voting me!")

def setup(bot):
    bot.add_cog(Bot_Info(bot))