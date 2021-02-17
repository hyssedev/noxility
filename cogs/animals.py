#pylint: disable=E0401
from discord.ext import commands
import asyncio, traceback, discord, inspect, textwrap, importlib, io, os, re, sys, copy, time, subprocess, platform, psutil, aiohttp
from contextlib import redirect_stdout
from psutil._common import bytes2human
import parsedatetime as pdt
from dateutil.relativedelta import relativedelta
from datetime import datetime
import utils.utils

class Animals (commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(aliases=["woof"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def dog(self, ctx):
        """Shows you a dog picture."""
        try:
            async with aiohttp.ClientSession() as cs:
                async with cs.get('https://dog.ceo/api/breeds/image/random') as r:
                    res = await r.json()
                    embed = discord.Embed(description="**Here is your dog picture. 🐶**", colour=0xf2c203)
                    embed.set_image(url=res['message'])
                    await ctx.send(embed=embed)
        except:
            raise discord.errors.Forbidden

    @commands.command(aliases=["meow"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def cat(self, ctx):
        """Shows you a cat picture."""
        try:
            async with aiohttp.ClientSession(headers={}) as cs:
                async with cs.get('https://api.thecatapi.com/v1/images/search') as r:
                    res = await r.json()
                    embed = discord.Embed(description="**Here is your cat picture. 🐱**", colour=0xf2c203)
                    embed.set_image(url=res[0]['url'])
                    await ctx.send(embed=embed)
        except:
            raise discord.errors.Forbidden

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def fox(self, ctx):
        """Shows you a fox picture."""
        try:
            async with aiohttp.ClientSession(headers={}) as cs:
                async with cs.get('https://some-random-api.ml/img/fox') as r:
                    res = await r.json()
                    embed = discord.Embed(description="**Here is your fox picture. 🦊**", colour=0xf2c203)
                    embed.set_image(url=res['link'])
                    await ctx.send(embed=embed)
        except:
            raise discord.errors.Forbidden

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def panda(self, ctx):
        """Shows you a panda picture."""
        try:
            async with aiohttp.ClientSession(headers={}) as cs:
                async with cs.get('https://some-random-api.ml/img/panda') as r:
                    res = await r.json()
                    embed = discord.Embed(description="**Here is your panda picture. 🐼**", colour=0xf2c203)
                    embed.set_image(url=res['link'])
                    await ctx.send(embed=embed)
        except:
            raise discord.errors.Forbidden

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def redpanda(self, ctx):
        """Shows you a red panda picture."""
        try:
            async with aiohttp.ClientSession(headers={}) as cs:
                async with cs.get('https://some-random-api.ml/img/red_panda') as r:
                    res = await r.json()
                    embed = discord.Embed(description="**Here is your red panda picture.**", colour=0xf2c203)
                    embed.set_image(url=res['link'])
                    await ctx.send(embed=embed)
        except:
            raise discord.errors.Forbidden

    @commands.command(aliases=["birb"])
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def bird(self, ctx):
        """Shows you a red panda picture."""
        try:
            async with aiohttp.ClientSession(headers={}) as cs:
                async with cs.get('https://some-random-api.ml/img/birb') as r:
                    res = await r.json()
                    embed = discord.Embed(description="**Here is your bird picture. 🐦**", colour=0xf2c203)
                    embed.set_image(url=res['link'])
                    await ctx.send(embed=embed)
        except:
            raise discord.errors.Forbidden

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def koala(self, ctx):
        """Shows you a koala picture."""
        try:
            async with aiohttp.ClientSession(headers={}) as cs:
                async with cs.get('https://some-random-api.ml/img/koala') as r:
                    res = await r.json()
                    embed = discord.Embed(description="**Here is your koala picture. 🐨**", colour=0xf2c203)
                    embed.set_image(url=res['link'])
                    await ctx.send(embed=embed)
        except:
            raise discord.errors.Forbidden

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def dogfact(self, ctx):
        """Tells you a random dog fact."""
        try:
            async with aiohttp.ClientSession(headers={}) as cs:
                async with cs.get('https://some-random-api.ml/facts/dog') as r:
                    res = await r.json()
                    embed = discord.Embed(colour=0xf2c203)
                    embed.add_field(name="**Here is your random dog fact. 🐶**", value=res['fact'])
                    await ctx.send(embed=embed)
        except:
            raise discord.errors.Forbidden

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def catfact(self, ctx):
        """Tells you a random cat fact."""
        try:
            async with aiohttp.ClientSession(headers={}) as cs:
                async with cs.get('https://some-random-api.ml/facts/cat') as r:
                    res = await r.json()
                    embed = discord.Embed(colour=0xf2c203)
                    embed.add_field(name="**Here is your random cat fact. 🐱**", value=res['fact'])
                    await ctx.send(embed=embed)
        except:
            raise discord.errors.Forbidden

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def pandafact(self, ctx):
        """Tells you a random panda fact."""
        try:
            async with aiohttp.ClientSession(headers={}) as cs:
                async with cs.get('https://some-random-api.ml/facts/panda') as r:
                    res = await r.json()
                    embed = discord.Embed(colour=0xf2c203)
                    embed.add_field(name="**Here is your random panda fact. 🐼**", value=res['fact'])
                    await ctx.send(embed=embed)
        except:
            raise discord.errors.Forbidden

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def foxfact(self, ctx):
        """Tells you a random fox fact."""
        try:
            async with aiohttp.ClientSession(headers={}) as cs:
                async with cs.get('https://some-random-api.ml/facts/fox') as r:
                    res = await r.json()
                    embed = discord.Embed(colour=0xf2c203)
                    embed.add_field(name="**Here is your random fox fact. 🦊**", value=res['fact'])
                    await ctx.send(embed=embed)
        except:
            raise discord.errors.Forbidden

def setup(bot):
    bot.add_cog(Animals(bot))