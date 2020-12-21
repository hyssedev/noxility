#pylint: disable=E0401
from discord.ext import commands
import asyncio, traceback, discord, inspect, textwrap, importlib, io, os, re, sys, copy, time, subprocess, platform, psutil, random, aiohttp
from contextlib import redirect_stdout
from psutil._common import bytes2human
import parsedatetime as pdt
from dateutil.relativedelta import relativedelta
from datetime import datetime
import utils.utils

class Fun (commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["pp", "ppsize"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def penis(self, ctx, member:discord.Member=None):
        """Shows you the specified users pp size."""
        if member == ctx.guild.me: return await ctx.send("Error, you can't use this on myself.", delete_after=5)
        member = ctx.author if not member else member
        embed = discord.Embed(colour=0xf2c203)
        size = random.randint(1, 20)
        embed.add_field(name="PP size", value=f"{member.name+'`s' if member != ctx.author else 'Your'} PP size is **{size}cm**.\n8{'='*int(size/2)}D")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def howgay(self, ctx, member:discord.Member=None):
        """Shows you how gay the specified user is."""
        if member == ctx.guild.me: return await ctx.send("Error, you can't use this on myself.", delete_after=5)
        member = ctx.author if not member else member
        embed = discord.Embed(colour=0xf2c203)
        embed.add_field(name="Gay checker", value=f"{member.name+' is' if member != ctx.author else 'You are'} **{random.randint(0, 100)}%** gay.")
        await ctx.send(embed=embed)

    @commands.command(name="8ball")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ball(self, ctx, args=None):
        """Tells you the bot's opinion to your answers."""
        if args == None: return await ctx.send("What do you want to ask me?", delete_after=5)
        answers = ['As I see it, yes.', 'Ask again later.', 'Better not tell you now.', 'Cannot predict now.', 'Concentrate and ask again.', 'Don’t count on it.', 'It is certain.', 'It is decidedly so.', 'Most likely.', 'My reply is no.', 'My sources say no.', 'Reply hazy, try again.', 'Signs point to yes.', 'Very doubtful.', 'Without a doubt.', 'Yes.', 'You may rely on it.', 'Yes – definitely.']
        await ctx.send(random.choice(answers))

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def clap(self, ctx, *, text=None):
        """Inserts clapping emojis between your words."""
        if text == None: return
        if " " not in text: return await ctx.send("Error, I need at least a space to replace.", delete_after=5)
        await ctx.send(text.replace(' ', ' \U0001f44f ')+f"\n\n**-- from {ctx.author.name}#{ctx.author.discriminator}**")

    @commands.command(aliases=["stink"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def stinky(self, ctx, member:discord.Member=None):
        """Shows you how stinky the specified user is."""
        if member == ctx.guild.me: return await ctx.send("Error, you can't use this on myself.", delete_after=5)
        member = ctx.author if not member else member
        embed = discord.Embed(colour=0xf2c203)
        embed.add_field(name="Stink checker", value=f"{member.name+' is' if member != ctx.author else 'You are'} **{random.randint(0, 100)}%** stinky.")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def simp(self, ctx, member:discord.Member=None):
        """Shows you how simp the specified user is."""
        if member == ctx.guild.me: return await ctx.send("Error, you can't use this on myself.", delete_after=5)
        member = ctx.author if not member else member
        embed = discord.Embed(colour=0xf2c203)
        embed.add_field(name="SIMP checker", value=f"{member.name+' is' if member != ctx.author else 'You are'} **{random.randint(0, 100)}%** simp.")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def howsad(self, ctx, member:discord.Member=None):
        """Shows you how sad the specified user is."""
        if member == ctx.guild.me: return await ctx.send("Error, you can't use this on myself.", delete_after=5)
        member = ctx.author if not member else member
        embed = discord.Embed(colour=0xf2c203)
        embed.add_field(name="Sad checker", value=f"{member.name+' is' if member != ctx.author else 'You are'} **{random.randint(0, 100)}%** sad.")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def hot(self, ctx, member:discord.Member=None):
        """Shows you how hot the specified user is."""
        if member == ctx.guild.me: return await ctx.send("Error, you can't use this on myself.", delete_after=5)
        member = ctx.author if not member else member
        embed = discord.Embed(colour=0xf2c203)
        embed.add_field(name="Hot checker", value=f"{member.name+' is' if member != ctx.author else 'You are'} **{random.randint(0, 100)}%** hot.")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def dadjoke(self, ctx):
        """Tells you a dad joke."""
        try:
            async with aiohttp.ClientSession(headers={"Accept":"application/json"}) as cs:
                async with cs.get('https://icanhazdadjoke.com/') as r:
                    res = await r.json()
                    await ctx.send(res['joke'])
        except:
            raise discord.errors.Forbidden

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def uselessfact(self, ctx):
        """Tells you a useless fact."""
        try:
            async with aiohttp.ClientSession() as cs:
                async with cs.get('https://uselessfacts.jsph.pl/random.json?language=en') as r:
                    res = await r.json()
                    await ctx.send(res['text'])
        except:
            raise discord.errors.Forbidden

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def reverse(self, ctx, *, text=None):
        """.txet deificeps sesreveR"""
        if text == None: return
        await ctx.send(str(text)[::-1])

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def pee(self, ctx, member:discord.Member=None):
        """Pee on someone."""
        if member == ctx.guild.me: return await ctx.send("Error, you can't use this on myself.", delete_after=5)
        member= ctx.author if not member else member
        await ctx.send(f"**{ctx.author.name}** peed on **{'himself' if member == ctx.author else member.name}**.")

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def poop(self, ctx, member:discord.Member=None):
        """Poop on someone."""
        if member == ctx.guild.me: return await ctx.send("Error, you can't use this on myself.", delete_after=5)
        member= ctx.author if not member else member
        await ctx.send(f"**{ctx.author.name}** pooped on **{'himself' if member == ctx.author else member.name}**.")

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def coinflip(self, ctx):
        """Flip a coin."""
        await ctx.send(f"You flipped a coin and it landed on **{random.choice(['tails', 'heads'])}**.")

def setup(bot):
    bot.add_cog(Fun(bot))