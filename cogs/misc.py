#pylint: disable=E0401
from discord.ext import commands
import asyncio, traceback, discord, inspect, textwrap, importlib, io, os, re, sys, copy, time, subprocess, platform, psutil, aiohttp
from contextlib import redirect_stdout
from psutil._common import bytes2human
import parsedatetime as pdt
from dateutil.relativedelta import relativedelta
from datetime import datetime

import utils.utils

class Misc (commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    async def weather(self, ctx, *, city:str):
        """Shows the current weather of the specified city."""
        link = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid=d36f33cd74759e0c9960f51db264bc93&units=metric'
        try:
            async with aiohttp.ClientSession() as cs:
                async with cs.get(link) as r:
                    res = await r.json()
                    embed=discord.Embed(colour=0xf2c203, title=f"Weather in {city.capitalize()} ({res['sys']['country']})", description=f"Weather condition: **{res['weather'][0]['main']}, {res['weather'][0]['description']}**")
                    embed.set_thumbnail(url=f"http://openweathermap.org/img/w/{res['weather'][0]['icon']}.png")
                    embed.add_field(name="Latitude", value=f"{res['coord']['lat']}")
                    embed.add_field(name="Longitude", value=f"{res['coord']['lon']}")
                    # embed.add_field(name="Timezone", value=f"{res['timezone']}")
                    embed.add_field(name="Current Temperature", value=f"{res['main']['temp']}°C / {round(((float(res['main']['temp'])*9/5)+32), 1)}°F")
                    embed.add_field(name="Feels like", value=f"{res['main']['feels_like']}°C / {round(((float(res['main']['feels_like'])*9/5)+32), 1)}°F")
                    embed.add_field(name="Visibility", value=f"{int(res['visibility']/1000)} KM")
                    embed.add_field(name="Min. temp", value=f"{res['main']['temp_min']}°C / {round(((float(res['main']['temp_min'])*9/5)+32), 1)}°F")
                    embed.add_field(name="Max. temp", value=f"{res['main']['temp_max']}°C / {round(((float(res['main']['temp_max'])*9/5)+32), 1)}°F")
                    embed.add_field(name="Wind Speed", value=f"{int(res['wind']['speed'])} KM/h / {int(res['wind']['speed']/1.609)} MPH")
                    embed.add_field(name="Wind Direction", value=f"{utils.utils.degToCompass(int(res['wind']['deg']))}")
                    embed.add_field(name="Atmospheric Pressure", value=f"{res['main']['pressure']} hPa")
                    embed.add_field(name="Humidity", value=f"{res['main']['humidity']}%")
                    embed.add_field(name="Clouds", value=f"{res['clouds']['all']}%")
                    #await ctx.send(res)
        except:
            raise discord.errors.Forbidden
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Misc(bot))