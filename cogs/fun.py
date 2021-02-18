#pylint: disable=E0401
from discord.ext import commands
import asyncio, traceback, discord, inspect, textwrap, importlib, io, os, re, sys, copy, time, subprocess, platform, psutil, random, aiohttp, dbl
from contextlib import redirect_stdout
from psutil._common import bytes2human
import parsedatetime as pdt
from dateutil.relativedelta import relativedelta
from datetime import datetime
import utils.utils

# MOVE ALL THESE INTO UTILS

def capitalize_2nd(s):
        ret = ""
        i = True  # capitalize
        for char in s:
            if i: ret += char.lower()
            else: ret += char.upper()
            if char != ' ': i = not i
        return ret

uselessweb = {
	"author": "@twholman - http://www.theuselessweb.com/",
	"uselessweb": ["http://heeeeeeeey.com/","http://thatsthefinger.com/","http://cant-not-tweet-this.com/","http://eelslap.com/","http://www.staggeringbeauty.com/","http://burymewithmymoney.com/","http://www.fallingfalling.com/","http://ducksarethebest.com/","http://www.trypap.com/","http://www.republiquedesmangues.fr/","http://www.movenowthinklater.com/","http://www.partridgegetslucky.com/","http://www.rrrgggbbb.com/","http://beesbeesbees.com/","http://www.sanger.dk/", "http://www.koalastothemax.com/", "http://www.everydayim.com/", "http://www.leduchamp.com/", "http://grandpanoclothes.com/", "http://www.haneke.net/", "http://instantostrich.com/", "http://r33b.net/", "http://randomcolour.com/", "http://cat-bounce.com/", "http://cachemonet.com/", "http://www.sadforjapan.com/", "http://www.taghua.com/", "http://chrismckenzie.com/", "http://hasthelargehadroncolliderdestroyedtheworldyet.com/", "http://ninjaflex.com/", "http://iloveyoulikeafatladylovesapples.com/", "http://ihasabucket.com/", "http://corndogoncorndog.com/", "http://giantbatfarts.com/", "http://www.ringingtelephone.com/", "http://www.pointerpointer.com/", "http://www.pleasedonate.biz/", "http://imaninja.com/", "http://willthefuturebeaweso.me/", "http://salmonofcapistrano.com/", "http://www.ismycomputeron.com/", "http://www.ooooiiii.com/", "http://www.wwwdotcom.com/", "http://www.nullingthevoid.com/", "http://www.muchbetterthanthis.com/", "http://www.ouaismaisbon.ch/", "http://iamawesome.com/", "http://www.pleaselike.com/", "http://crouton.net/", "http://corgiorgy.com/", "http://www.electricboogiewoogie.com/", "http://www.nelson-haha.com/", "http://www.wutdafuk.com/", "http://unicodesnowmanforyou.com/", "http://tencents.info/", "http://intotime.com/", "http://leekspin.com/", "http://minecraftstal.com/", "http://www.riddlydiddly.com/", "http://www.patience-is-a-virtue.org/", "http://whitetrash.nl/", "http://www.theendofreason.com/", "http://zombo.com", "http://secretsfornicotine.com/", "http://pixelsfighting.com/", "http://crapo.la/", "http://baconsizzling.com/", "http://isitwhite.com/", "http://noot.space/", "http://tomsdog.com/", "http://goat.com/","https://www.dialupsound.com/","http://computerpowertest.com/","http://www.eeyup.com/","http://www.nevernowhere.com/","http://make-everything-ok.com/","http://thenicestplaceontheinter.net/","http://www.nyan.cat/","http://zombo.com/","http://gprime.net/game.php/dodgethedot","http://blank.org/","http://www.thedancinglion.com/","http://touchpianist.com/","http://www.whatsmystarbucksname.com/","http://time.tetrasign.com/emojiclock/","http://2015.tetrasign.com/","http://www.youcanseethemilkyway.com/","http://kolor.moro.es/","http://foaas.com/"]
}

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
    
    async def fun_checker(self, cmd:str, member=None):
        if cmd == 'penis': return random.randint(1, 20) if not await self.bot.dblpy.get_user_vote(member.id) else random.randint(6, 20)
        elif cmd == 'howgay': return random.randint(0, 100) if not await self.bot.dblpy.get_user_vote(member.id) else random.randint(0, 70)
        elif cmd == 'stinky': return random.randint(0, 100) if not await self.bot.dblpy.get_user_vote(member.id) else random.randint(0, 70)
        elif cmd == 'simp': return random.randint(0, 100) if not await self.bot.dblpy.get_user_vote(member.id) else random.randint(0, 70)
        elif cmd == 'howsad': return random.randint(0, 100) if not await self.bot.dblpy.get_user_vote(member.id) else random.randint(0, 70)
        elif cmd == 'hot': return random.randint(0, 100) if not await self.bot.dblpy.get_user_vote(member.id) else random.randint(30, 100)
        elif cmd == 'from': return f'\n\n**-- from {member.name}#{member.discriminator}**' if not await self.bot.dblpy.get_user_vote(member.id) else ''

    async def tip(self, ctx):
        if not await self.bot.dblpy.get_user_vote(ctx.author.id):
            return f'\n\n**For voting, you receive 30% better odds, in your favor, for fun commands and more! You can type `nox vote` to vote and get these benefits!**'  if random.randint(0,3) == 3 else ' ' 
        else:
            return ''

    @commands.command(aliases=["pp", "ppsize"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def penis(self, ctx, member:discord.Member=None):
        """Shows you the specified users pp size."""
        if member == ctx.guild.me: return await ctx.send("Error, you can't use this on myself.", delete_after=5)
        member = ctx.author if not member else member 
        embed = discord.Embed(colour=0xf2c203)
        size = await Fun.fun_checker(self, 'penis', member)
        embed.add_field(name="PP size", value=f"{member.name if member != ctx.author else ctx.author.name}'s PP size is **{size}cm**.\n8{'='*int(size/2)}D{await Fun.tip(self, ctx)}")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def howgay(self, ctx, member:discord.Member=None):
        """Shows you how gay the specified user is."""
        if member == ctx.guild.me: return await ctx.send("Error, you can't use this on myself.", delete_after=5)
        member = ctx.author if not member else member
        embed = discord.Embed(colour=0xf2c203)
        embed.add_field(name="Gay checker", value=f"{member.name if member != ctx.author else ctx.author.name} is **{await Fun.fun_checker(self, 'howgay', member)}%** gay.{await Fun.tip(self, ctx)}")
        await ctx.send(embed=embed)

    @commands.command(name="8ball")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def ball(self, ctx, args=None):
        """Tells you the bot's opinion to your answers."""
        if args == None: return await ctx.send("What do you want to ask me?", delete_after=5)
        answers = ['As I see it, yes.', 'Ask again later.', 'Better not tell you now.', 'Cannot predict now.', 'Concentrate and ask again.', 'Don’t count on it.', 'It is certain.', 'It is decidedly so.', 'Most likely.', 'My reply is no.', 'My sources say no.', 'Reply hazy, try again.', 'Signs point to yes.', 'Very doubtful.', 'Without a doubt.', 'Yes.', 'You may rely on it.', 'Yes – definitely.']
        await ctx.send(f"{random.choice(answers)}{await Fun.tip(self, ctx)}")

    @commands.command()
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def clap(self, ctx, *, text=None):
        """Inserts clapping emojis between your words."""
        if text == None: return
        if " " not in text: return await ctx.send("Error, I need at least a space to replace.", delete_after=5)
        await ctx.send(text.replace(' ', ' \U0001f44f ')+ f"{await Fun.fun_checker(self, 'from', ctx.author)}{await Fun.tip(self, ctx)}")

    @commands.command(aliases=["stink"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def stinky(self, ctx, member:discord.Member=None):
        """Shows you how stinky the specified user is."""
        if member == ctx.guild.me: return await ctx.send("Error, you can't use this on myself.", delete_after=5)
        member = ctx.author if not member else member
        embed = discord.Embed(colour=0xf2c203)
        embed.add_field(name="Stink checker", value=f"{member.name if member != ctx.author else ctx.author.name} is **{await Fun.fun_checker(self, 'stinky', member)}%** stinky.{await Fun.tip(self, ctx)}")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def simp(self, ctx, member:discord.Member=None):
        """Shows you how simp the specified user is."""
        if member == ctx.guild.me: return await ctx.send("Error, you can't use this on myself.", delete_after=5)
        member = ctx.author if not member else member
        embed = discord.Embed(colour=0xf2c203)
        embed.add_field(name="SIMP checker", value=f"{member.name if member != ctx.author else ctx.author.name} is **{await Fun.fun_checker(self, 'simp', member)}%** simp.{await Fun.tip(self, ctx)}")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def howsad(self, ctx, member:discord.Member=None):
        """Shows you how sad the specified user is."""
        if member == ctx.guild.me: return await ctx.send("Error, you can't use this on myself.", delete_after=5)
        member = ctx.author if not member else member
        embed = discord.Embed(colour=0xf2c203)
        embed.add_field(name="Sad checker", value=f"{member.name if member != ctx.author else ctx.author.name} is **{await Fun.fun_checker(self, 'howsad', member)}%** sad.{await Fun.tip(self, ctx)}")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def hot(self, ctx, member:discord.Member=None):
        """Shows you how hot the specified user is."""
        if member == ctx.guild.me: return await ctx.send("Error, you can't use this on myself.", delete_after=5)
        member = ctx.author if not member else member
        embed = discord.Embed(colour=0xf2c203)
        embed.add_field(name="Hot checker", value=f"{member.name if member != ctx.author else ctx.author.name} is **{await Fun.fun_checker(self, 'hot', member)}%** hot.{await Fun.tip(self, ctx)}")
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
        await ctx.send(f"{str(text)[::-1]}{await Fun.fun_checker(self, 'from', ctx.author)}{await Fun.tip(self, ctx)}")

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def pee(self, ctx, member:discord.Member=None):
        """Pee on someone."""
        if member == ctx.guild.me: return await ctx.send("Error, you can't use this on myself.", delete_after=5)
        member= ctx.author if not member else member
        await ctx.send(f"**{ctx.author.name}** peed on **{'himself' if member == ctx.author else member.name}**.{await Fun.tip(self, ctx)}")

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def poop(self, ctx, member:discord.Member=None):
        """Poop on someone."""
        if member == ctx.guild.me: return await ctx.send("Error, you can't use this on myself.", delete_after=5)
        member= ctx.author if not member else member
        await ctx.send(f"**{ctx.author.name}** pooped on **{'himself' if member == ctx.author else member.name}**.{await Fun.tip(self, ctx)}")

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def coinflip(self, ctx):
        """Flip a coin."""
        await ctx.send(f"You flipped a coin and it landed on **{random.choice(['tails', 'heads'])}**.{await Fun.tip(self, ctx)}")

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def emojify(self, ctx, *, text=None):
        """Emojifies the specified text."""
        if text == None: return await ctx.send("What text do you want me to emojify?")
        msg = list(text)
        regional_list = [self.regionals[x.lower()] if x.isalnum() or x in ["!", "?"] else x for x in msg]
        regional_output = '\u200b'.join(regional_list)
        await ctx.send(f"{regional_output}{await Fun.fun_checker(self, 'from', ctx.author)}{await Fun.tip(self, ctx)}")

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def leetify(self, ctx, *, text=None):
        """Will leetify text."""
        if text == None: return await ctx.send("What text do you want me to leetify?")
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
        await ctx.send(f"{text}{await Fun.fun_checker(self, 'from', ctx.author)}{await Fun.tip(self, ctx)}")

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def mock(self, ctx, *, text=None):
        """Will mock a user."""
        if text == None: return await ctx.send("What text do you want me to mock?")
        await ctx.send(f"{capitalize_2nd(text)}\nhttps://pyxis.nymag.com/v1/imgs/09c/923/65324bb3906b6865f904a72f8f8a908541-16-spongebob-explainer.rsquare.w700.jpg{await Fun.fun_checker(self, 'from', ctx.author)}{await Fun.tip(self, ctx)}")

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def uselessweb(self, ctx):
        """Returns a random useless site."""
        await ctx.send(random.choice(uselessweb['uselessweb']))

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def spoiler(self, ctx, *, text=None):
        """Returns the text, but spoilered."""
        if text == None: return await ctx.send("What text do you want me to return spoilered?")
        for word in text.split():
            text = text.replace(word, f"||{word}||")
        await ctx.send(f"{text}{await Fun.fun_checker(self, 'from', ctx.author)}{await Fun.tip(self, ctx)}")

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def choose(self, ctx, *, text=None):
        """Returns what the bot has chosen. To be able to use this command, separate your options with `|`."""
        if text == None: return await ctx.send("What choices do you give me?")
        choice = random.choice(text.split("|"))
        await ctx.send(f"I choose: **{choice}**{await Fun.fun_checker(self, 'from', ctx.author)}{await Fun.tip(self, ctx)}")
    
    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def wink(self, ctx):
        """Returns a winking picture or gif."""
        try:
            async with aiohttp.ClientSession(headers={}) as cs:
                async with cs.get('https://some-random-api.ml/animu/wink') as r:
                    res = await r.json()
                    embed = discord.Embed(description="**wink wink UwU**", colour=0xf2c203)
                    embed.set_image(url=res['link'])
                    await ctx.send(embed=embed)
        except:
            raise discord.errors.Forbidden

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def pat(self, ctx, member: discord.Member = None):
        """Returns a patting picture or gif."""
        if member == None: return await ctx.send("Error, who do you want to pat?", delete_after=5)
        try:
            async with aiohttp.ClientSession(headers={}) as cs:
                async with cs.get('https://some-random-api.ml/animu/pat') as r:
                    res = await r.json()
                    embed = discord.Embed(description=f"**{ctx.author.name} patted {member.name} on his head**", colour=0xf2c203)
                    embed.set_image(url=res['link'])
                    await ctx.send(embed=embed)
        except:
            raise discord.errors.Forbidden

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def hug(self, ctx, member: discord.Member = None):
        """Returns a hugging picture or gif."""
        if member == None: return await ctx.send("Error, who do you want to hug?", delete_after=5)
        try:
            async with aiohttp.ClientSession(headers={}) as cs:
                async with cs.get('https://some-random-api.ml/animu/hug') as r:
                    res = await r.json()
                    embed = discord.Embed(description=f"**{ctx.author.name} hugged {member.name}**", colour=0xf2c203)
                    embed.set_image(url=res['link'])
                    await ctx.send(embed=embed)
        except:
            raise discord.errors.Forbidden

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def hug(self, ctx, member: discord.Member = None):
        """Returns a gay picture or gif of the specified user."""
        member = ctx.author if not member else member
        embed = discord.Embed(colour=0xf2c203)
        try:
            embed.set_image(url=f'https://some-random-api.ml/canvas/gay?avatar={member.avatar_url_as(format='png')}')
        except:
            raise discord.errors.Forbidden

def setup(bot):
    bot.add_cog(Fun(bot))