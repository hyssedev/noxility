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
        self.regionals = {'a': '\N{REGIONAL INDICATOR SYMBOL LETTER A}', 'b': '\N{REGIONAL INDICATOR SYMBOL LETTER B}',
                          'c': '\N{REGIONAL INDICATOR SYMBOL LETTER C}',
                          'd': '\N{REGIONAL INDICATOR SYMBOL LETTER D}', 'e': '\N{REGIONAL INDICATOR SYMBOL LETTER E}',
                          'f': '\N{REGIONAL INDICATOR SYMBOL LETTER F}',
                          'g': '\N{REGIONAL INDICATOR SYMBOL LETTER G}', 'h': '\N{REGIONAL INDICATOR SYMBOL LETTER H}',
                          'i': '\N{REGIONAL INDICATOR SYMBOL LETTER I}',
                          'j': '\N{REGIONAL INDICATOR SYMBOL LETTER J}', 'k': '\N{REGIONAL INDICATOR SYMBOL LETTER K}',
                          'l': '\N{REGIONAL INDICATOR SYMBOL LETTER L}',
                          'm': '\N{REGIONAL INDICATOR SYMBOL LETTER M}', 'n': '\N{REGIONAL INDICATOR SYMBOL LETTER N}',
                          'o': '\N{REGIONAL INDICATOR SYMBOL LETTER O}',
                          'p': '\N{REGIONAL INDICATOR SYMBOL LETTER P}', 'q': '\N{REGIONAL INDICATOR SYMBOL LETTER Q}',
                          'r': '\N{REGIONAL INDICATOR SYMBOL LETTER R}',
                          's': '\N{REGIONAL INDICATOR SYMBOL LETTER S}', 't': '\N{REGIONAL INDICATOR SYMBOL LETTER T}',
                          'u': '\N{REGIONAL INDICATOR SYMBOL LETTER U}',
                          'v': '\N{REGIONAL INDICATOR SYMBOL LETTER V}', 'w': '\N{REGIONAL INDICATOR SYMBOL LETTER W}',
                          'x': '\N{REGIONAL INDICATOR SYMBOL LETTER X}',
                          'y': '\N{REGIONAL INDICATOR SYMBOL LETTER Y}', 'z': '\N{REGIONAL INDICATOR SYMBOL LETTER Z}',
                          '0': '0⃣', '1': '1⃣', '2': '2⃣', '3': '3⃣',
                          '4': '4⃣', '5': '5⃣', '6': '6⃣', '7': '7⃣', '8': '8⃣', '9': '9⃣', '!': '\u2757',
                          '?': '\u2753'}

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

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def dog(self, ctx):
        """Shows you a dog picture."""
        try:
            async with aiohttp.ClientSession() as cs:
                async with cs.get('https://dog.ceo/api/breeds/image/random') as r:
                    res = await r.json()
                    await ctx.send(res['message'])
        except:
            raise discord.errors.Forbidden

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def cat(self, ctx):
        """Shows you a cat picture."""
        try:
            async with aiohttp.ClientSession(headers={}) as cs:
                async with cs.get('https://api.thecatapi.com/v1/images/search') as r:
                    res = await r.json()
                    await ctx.send(res[0]['url'])
        except:
            raise discord.errors.Forbidden

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def emojify(self, ctx, *, text=None):
        """Emojifies the specified text."""
        if text == None: return
        msg = list(text)
        regional_list = [self.regionals[x.lower()] if x.isalnum() or x in ["!", "?"] else x for x in msg]
        regional_output = '\u200b'.join(regional_list)
        await ctx.send(regional_output)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def leetify(self, ctx, *, text=None):
        if text == None: return
        for char in text:
            if char == 'a': text = text.replace('a','4')
            elif char == 'b': text = text.replace('b','8')
            elif char == 'e': text = text.replace('e','3')
            elif char == 'l': text = text.replace('l','1')
            elif char == 'o': text = text.replace('o','0')
            elif char == 's': text = text.replace('s','5')
            elif char == 't': text = text.replace('t','7')
            else:
                pass
        await ctx.send(text)

def setup(bot):
    bot.add_cog(Fun(bot))