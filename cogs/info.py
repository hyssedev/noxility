#pylint: disable=E0401
from discord.ext import commands
import asyncio, traceback, discord, inspect, textwrap, importlib, io, os, re, sys, copy, time, subprocess, platform, psutil, datetime
from contextlib import redirect_stdout
from psutil._common import bytes2human
import parsedatetime as pdt
from dateutil.relativedelta import relativedelta
from utils.utils import human_timedelta
from utils.utils import emote
import utils.utils

class Info (commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group(invoke_without_command=False)
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def guild(self, ctx):
        """Command group for many different guild related commands."""
        if ctx.invoked_subcommand == None: await ctx.send("Error, this command requires at least 1 argument.")

    @guild.command(name="info")
    async def infooo(self, ctx):
        """Shows info about current server."""
        try:
            bans = len(await ctx.guild.bans())
        except:
            bans = "No permission."
        created = (ctx.guild.created_at).strftime("%d %B, %Y")
        embed = discord.Embed(colour=0xf2c203)
        embed.set_thumbnail(url=f"{ctx.guild.icon_url}")
        embed.add_field(name=f"**General Info**", value=f"{emote} **Name:** {ctx.guild.name}\n{emote} **Description:** {ctx.guild.description}\n{emote} **ID:** {ctx.guild.id}\n{emote} **Region:** {ctx.guild.region}\n{emote} **Verification Level:** {str(ctx.guild.verification_level).capitalize()}\n{emote} **Upload Limit:** {bytes2human(ctx.guild.filesize_limit)}B\n{emote} **Channels:** {len(ctx.guild.text_channels)} Text | {len(ctx.guild.voice_channels)} Voice\n{emote} **Emojis:** {len(ctx.guild.emojis)}/{ctx.guild.emoji_limit}\n{emote} **Created:** {created} ({utils.utils.human_timedelta(ctx.guild.created_at)} ago)\n{emote} **Shard ID:** {ctx.guild.shard_id}\n{emote} **Boosters:** {ctx.guild.premium_subscription_count}\n{emote} **Boost Level:** {ctx.guild.premium_tier}", inline=False)
        embed.add_field(name=f"**Member Info**", value=f"{emote} **Owner:** {ctx.guild.owner.name}#{ctx.guild.owner.discriminator}\n{emote} **Members:** {len(ctx.guild.members)} ({len([i for i in ctx.guild.members if i.status != discord.Status.offline])} online)\n{emote} **Bans:** {bans}\n{emote} **Roles:** {len(ctx.guild.roles)}", inline=False)
        await ctx.send(embed=embed)

    @guild.command()
    async def banner(self, ctx):
        """Retrieves the current guild's icon."""
        if not ctx.guild.banner: return await ctx.send("Error, this server does not have a banner.")
        embed = discord.Embed(title=f"{ctx.guild.name}'s banner", color=0xf2c203, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.set_image(url=f'{ctx.guild.banner_url}')
        await ctx.send(embed=embed)

    @guild.command()
    async def icon(self, ctx):
        """Retrieves the current guild's banner."""
        if not ctx.guild.icon: return await ctx.send("Error, this server does not have an icon.")
        embed = discord.Embed(title=f"{ctx.guild.name}'s icon", color=0xf2c203, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.set_image(url=f'{ctx.guild.icon_url}')
        await ctx.send(embed=embed)

    @commands.group(invoke_without_command=False)
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def channel(self, ctx):
        """Command group for many different channel related commands."""
        if ctx.invoked_subcommand == None: await ctx.send("Error, this command requires at least 1 argument.")

    @channel.command(name="info")
    async def _info(self, ctx):
        """Retrieves info about current channel."""
        embed = discord.Embed(title=f"Stats for **{ctx.channel.name}**", description=f"Category: {ctx.channel.category.name if ctx.channel.category else 'No category'}", color=0xf2c203)
        embed.add_field(name="Guild", value=ctx.guild.name, inline=False)
        embed.add_field(name="ID", value=ctx.channel.id, inline=False)
        embed.add_field(name="Topic", value=f"{ctx.channel.topic if ctx.channel.topic else 'No topic.'}", inline=False)
        embed.add_field(name="Position", value=ctx.channel.position, inline=False)
        embed.add_field(name="Slowmode Delay", value=ctx.channel.slowmode_delay, inline=False)
        embed.add_field(name="NSFW", value=ctx.channel.is_nsfw(), inline=False)
        embed.add_field(name="NEWS", value=ctx.channel.is_news(), inline=False)
        embed.add_field(name="Creation Time", value=ctx.channel.created_at.strftime("%d %B, %Y"), inline=False)
        embed.add_field(name="Permissions Synced", value=ctx.channel.permissions_synced, inline=False)
        embed.add_field(name="Hash", value=hash(ctx.channel), inline=False)
        await ctx.send(embed=embed)

    @channel.command(name="list")
    async def _list(self, ctx):
        """Retrieves a list about current guilds channels."""
        # channels = ", ".join([str(x) for x in ctx.guild.channels])
        channels = ""
        embed = discord.Embed(colour=0xf2c203)
        for index, channel in enumerate(ctx.guild.channels):
            if len(channels) >= 900:
                embed.set_footer(text=f"...and other {len(ctx.guild.channels) - index} channel{utils.utils.plural_check(len(ctx.guild.channels) - index)} (too many to show).")
                break
            channels += str(channel) + " "
        embed.add_field(name="Guild Channel List", value=f"**`[{len(ctx.guild.channels)}]` channel{utils.utils.plural_check(len(ctx.guild.channels))} of which {len(ctx.guild.text_channels)} text and {len(ctx.guild.voice_channels)} voice**\n{channels}")
        await ctx.send(embed=embed)

    @channel.command(name="slowmode")
    @commands.bot_has_permissions(manage_channels=True)
    @commands.has_guild_permissions(manage_channels=True)
    async def slowmodee(self, ctx, delay: str):
        """Sets current channels slowmode to specified amount of seconds."""
        if not delay.isnumeric(): return await ctx.send("Error, please enter a correct number.")
        if int(delay) > 21598: return await ctx.send("Error, invalid range.")
        await ctx.channel.edit(slowmode_delay=int(delay))
        m, s = divmod(int(delay), 60)
        h, m = divmod(m, 60)
        if int(delay) == 0:
            await ctx.send(f"✅ Successfully removed `{ctx.channel.name}'s` slowmode.") 
        elif int(h) == 0 and int(m) == 0:
            await ctx.send(f"✅ Successfully set `{ctx.channel.name}'s` slowmode to {int(s)} second{'s' if int(s) != 1 else ''}.")
        elif int(h) == 0 and int(m) != 0:
            await ctx.send(f"✅ Successfully set `{ctx.channel.name}'s` slowmode to {int(m)} minute{'s' if int(m) != 1 else ''} and {int(s)} second{'s' if int(s) != 1 else ''}.")
        else:
            await ctx.send(f"✅ Successfully set `{ctx.channel.name}'s` slowmode to {int(h)} hour{'s' if int(h) != 1 else ''}, {int(m)} minute{'s' if int(m) != 1 else ''} and {int(s)} second{'s' if int(s) != 1 else ''}.")

    @commands.group(invoke_without_command=False)
    @commands.guild_only()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def role(self, ctx):
        """Command group for many different role related commands."""
        if ctx.invoked_subcommand == None: await ctx.send("Error, this command requires at least 1 argument.")
        
    @role.command(name="info")
    async def info_(self, ctx, role:discord.Role):
        """Retrieves info about specified role."""
        created = (role.created_at).strftime("%d %B, %Y, %H:%M")
        owned_by = len(role.members)
        embed = discord.Embed(colour=role.colour)
        embed.add_field(name=f"**User**", value=f"{emote} **Mention:** {role.mention}\n{emote} **ID:** {role.id}\n{emote} **Owned by:** {owned_by} member{utils.utils.plural_check(owned_by)}\n{emote} **Created:** {created}\n{emote} **Position:** {role.position}\n{emote} **Hoisted:** {'<:noxcheck:787008166327615509>' if role.hoist else '<:noxcross1:787008036882350100>'}\n{emote} **Mentionable:** {'<:noxcheck:787008166327615509>' if role.mentionable else '<:noxcross1:787008036882350100>'}\n{emote} **Managed:** {'<:noxcheck:787008166327615509>' if role.managed else '<:noxcross1:787008036882350100>'}", inline=False)
        await ctx.send(embed=embed)

    @role.command(name="list")
    async def list_(self, ctx):
        """Retrieves a list about current guilds roles."""
        # roles = ", ".join([str(x) for x in ctx.guild.roles])
        roles = ""
        embed = discord.Embed(colour=0xf2c203)
        for index, role in enumerate(ctx.guild.roles):
            if len(roles) >= 950:
                embed.set_footer(text=f"...and other {len(ctx.guild.roles) - index} role{utils.utils.plural_check(len(ctx.guild.roles) - index)} (too many to show).")
                break
            roles += str(role) + " "
        embed.add_field(name="Guild Role List", value=f"**`[{len(ctx.guild.roles)}]` role{utils.utils.plural_check(len(ctx.guild.roles))}:** {roles}\n")
        await ctx.send(embed=embed)

    @role.command(name="add")
    @commands.bot_has_permissions(manage_roles=True)
    @commands.has_guild_permissions(manage_roles=True)
    async def _add(self, ctx, member: discord.Member, role: discord.Role):
        """Gives the specified member the specified role."""
        # no need to do try: except: because we already check for required permissions
        if role in member.roles: return await ctx.send("Error, this member already has that role!")
        await member.add_roles(role)
        await ctx.send(f"Gave {member.name} the {role.name} role.")

    @role.command(name="remove")
    @commands.bot_has_permissions(manage_roles=True)
    @commands.has_guild_permissions(manage_roles=True)
    async def _remove(self, ctx, member: discord.Member, role: discord.Role):
        """Removes the specified member the specified role."""
        if role not in member.roles: return await ctx.send("Error, this member does not have that role!")
        # no need to do try: except: because we already check for required permissions
        await member.remove_roles(role)
        await ctx.send(f"Removed {role.name} from {member.name} role.")

    @role.command(name="members")
    @commands.max_concurrency(1, per=commands.BucketType.default, wait=False)
    async def members(self, ctx, role: discord.Role):
        """Shows how many members have the specified role."""
        pages = []
        count = 1
        for i in range(0, len(role.members), 15):
            members = ""
            next_members = role.members[i : i + 15]
            for member in next_members:
                members += f"`[{count}]` **{member}** (ID: {member.id})\n"
                count += 1
            pages.append(members)
        pages2 = [s + f"\n`{len(pages)} page{utils.utils.plural_check(len(pages))}, {count-1} {'entries' if count-1 > 1 else 'entry'}`" for s in pages]
        await utils.utils.Pag(color=0xf2c203, entries=pages2, length=1, timeout=30).start(ctx)

    @commands.group(invoke_without_command=False)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def emoji(self, ctx):
        """Command group for many different emoji related commands."""
        if ctx.invoked_subcommand == None: await ctx.send("Error, this command requires at least 1 argument.")

    @emoji.command(name="list")
    async def __list(self, ctx):
        """Retrieves a list about current guilds emojis."""
        embed = discord.Embed(colour=0xf2c203)
        emojis = ""
        if len(ctx.guild.emojis)==0: return await ctx.send("Error, this guild doesn't have any emoji.")
        for index, emoji in enumerate(ctx.guild.emojis):
            if len(emojis) >= 1000:
                embed.set_footer(text=f"...and other {len(ctx.guild.emojis) - index} custom emoji{utils.utils.plural_check(len(ctx.guild.emojis) - index)} (too many to show).")
                break
            emojis += str(emoji) + " "
        embed.add_field(name=f"{ctx.guild.name} Custom Emojis List", value=f"{emojis}")
        await ctx.send(embed=embed)

    @emoji.command(name="info")
    async def __info(self, ctx, emoji:discord.Emoji):
        """Retrieves info about specified emoji."""
        # TIP: Does not work with emojis that are in servers that the bot is not in
        embed = discord.Embed(colour=0xf2c203)
        created = (emoji.created_at).strftime("%d %B, %Y")
        embed.set_thumbnail(url=f"{emoji.url}")
        embed.add_field(name="Emoji Info", value=f"{emote} **Name:** {emoji.name}\n{emote} **ID:** {emoji.id}\n{emote} **Created:** {created} ({utils.utils.human_timedelta(emoji.created_at)} ago)\n{emote} **Animated:** {'<:check:787008166327615509>' if emoji.animated else '<:cross1:787008036882350100>'}\n{emote} **URL:** [click here]({emoji.url})")
        await ctx.send(embed=embed)

    @emoji.command()
    async def enlarge(self, ctx, emoji:discord.Emoji):
        """Enlarges specified emoji."""
        # TIP: Does not work with emojis that are in servers that the bot is not in
        await ctx.send(f"{emoji.url}")

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def avatar(self, ctx, member: discord.Member=None):
        """Shows the avatar of the mentioned user."""
        member = ctx.author if not member else member
        embed = discord.Embed(colour=0xf2c203, description=f"[Avatar Link]({member.avatar_url})")
        embed.set_image(url=f"{member.avatar_url}")
        embed.set_author(name=f"{member.name}'s avatar", icon_url=f"{member.avatar_url}")
        embed.set_footer(text=f"Requested by {ctx.author.name}", icon_url=f"{ctx.author.avatar_url}")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def userinfo(self, ctx, member: discord.Member=None):
        """Shows info about the mentioned user."""
        member = ctx.author if not member else member
        embed = discord.Embed(colour=0xf2c203)
        created = (member.created_at).strftime("%d %B, %Y")
        joined = (member.joined_at).strftime("%d %B, %Y")
        embed.set_thumbnail(url=f"{member.avatar_url}")
        embed.add_field(name=f"**General Info**", value=f"{emote} **Full name:** {member.name}#{member.discriminator}\n{emote} **User ID:** {member.id}\n{emote} **Nickname:** {member.display_name if member.display_name != member.name else 'None'}\n{emote} **Roles:** {int(len(member.roles))-1}\n{emote} **Activity:** {member.activities[0] if member.activities else 'None'}\n{emote} **Joined Server:** {joined} ({utils.utils.human_timedelta(member.joined_at)} ago)\n{emote} **User Created:** {created} ({utils.utils.human_timedelta(member.created_at)} ago)\n{emote} **Bot:** {'<:check:787008166327615509>' if member.bot else '<:cross1:787008036882350100>'}\n{emote} **Avatar url:** [click here]({member.avatar_url})", inline=False)
        embed.add_field(name=f"**Status**", value=f"{utils.utils.check_status(member, 2)} | \U0001f4f1 Mobile Status\n{utils.utils.check_status(member, 3)} | \U0001f5a5 Desktop Status\n{utils.utils.check_status(member, 1)} | <:noxweb:787015386322960405> Web Status")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Info(bot))