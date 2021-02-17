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

    

def setup(bot):
    bot.add_cog(Animals(bot))