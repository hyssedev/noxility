from discord.ext import commands
import asyncio, traceback, discord, inspect, textwrap, importlib, io, os, re, sys, copy, time, subprocess, platform, psutil, datetime
from contextlib import redirect_stdout
from psutil._common import bytes2human
import parsedatetime as pdt
from dateutil.relativedelta import relativedelta
from cogs._utils import human_timedelta
import cogs._utils

emote = "<:noxilityarrow:786985788893560923>"

class Info (commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 20, commands.BucketType.user)
    async def guildbanner(self, ctx):
        """Retrieves the current guild's banner"""
        if not ctx.guild.icon: return await ctx.send("This server does not have a banner.")
        embed = discord.Embed(title=f"{ctx.guild.name}'s banner", color=0xf2c203, timestamp=ctx.message.created_at)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.set_image(url=f'{ctx.guild.banner_url}')
        await ctx.send(embed=embed)

    @commands.group(invoke_without_command=False)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def channel(self, ctx):
        """Command group for many different channel related commands."""
        if ctx.invoked_subcommand == None: await ctx.send("Error, this command requires at least 1 argument.")

    @channel.command()
    async def info(self, ctx):
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

    @channel.command()
    async def list(self, ctx):
        """Retrieves a list about current guilds channels."""
        channels = ", ".join([str(x) for x in ctx.guild.channels])
        embed = discord.Embed(colour=0xf2c203)
        embed.add_field(name="Guild Channel List", value=f"**`[{len(ctx.guild.channels)}]` channels of which {len(ctx.guild.text_channels)} text and {len(ctx.guild.voice_channels)} voice**\n{channels}") if len(channels) < 1000 else embed.add_field(name="Guild Channel List", value=f"**`[{len(ctx.guild.channels)}]` channels of which {len(ctx.guild.text_channels)} text and {len(ctx.guild.voice_channels)} voice**\nToo many to list them all!")
        await ctx.send(embed=embed)

    @commands.group(invoke_without_command=False)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def role(self, ctx):
        """Command group for many different role related commands."""
        if ctx.invoked_subcommand == None: await ctx.send("Error, this command requires at least 1 argument.")
        
    @role.command(name="info")
    async def _info(self, ctx, role:discord.Role):
        """Retrieves info about specified role."""
        created = (role.created_at).strftime("%d %B, %Y, %H:%M")
        owned_by = len(role.members)
        embed = discord.Embed(colour=role.colour)
        embed.add_field(name=f"**User**", value=f"{emote} **Mention:** {role.mention}\n{emote} **ID:** {role.id}\n{emote} **Owned by:** {owned_by} member{'s' if owned_by > 1 else ''}\n{emote} **Created:** {created}\n{emote} **Position:** {role.position}\n{emote} **Hoisted:** {'<:noxcheck:787008166327615509>' if role.hoist else '<:noxcross1:787008036882350100>'}\n{emote} **Mentionable:** {'<:noxcheck:787008166327615509>' if role.mentionable else '<:noxcross1:787008036882350100>'}\n{emote} **Managed:** {'<:noxcheck:787008166327615509>' if role.managed else '<:noxcross1:787008036882350100>'}", inline=False)
        await ctx.send(embed=embed)

    @role.command(name="list")
    async def _list(self, ctx):
        """Retrieves a list about current guilds roles"""
        roles = ", ".join([str(x) for x in ctx.guild.roles])
        embed = discord.Embed(colour=0xf2c203)
        roles = ""
        for index, role in enumerate(ctx.guild.roles):
            if len(roles) >= 950:
                embed.set_footer(text=f"...and other {len(ctx.guild.roles) - index} roles (too many to show).")
                break
            roles += str(role) + str(role) +" "
        embed.add_field(name="Guild Role List", value=f"**`[{len(ctx.guild.roles)}]` roles:** {roles}\n")
        await ctx.send(embed=embed)

    @role.command(name="add")
    async def _add(self, ctx, member: discord.Member, role: discord.Role):
        """Gives the specified member the specified role."""
        pass

    @role.command(name="remove")
    async def _remove(self, ctx, member: discord.Member, role: discord.Role):
        """Removes the specified member the specified role."""
        pass

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
        pages2 = [s + f"\n`{len(pages)} page{'s' if len(pages) > 1 else ''}, {count-1} {'entries' if count-1 > 1 else 'entry'}`" for s in pages]
        await cogs._utils.Pag(color=0xf2c203, entries=pages2, length=1, timeout=30).start(ctx)

    @commands.group(invoke_without_command=False)
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def emoji(self, ctx):
        """Command group for many different emoji related commands."""
        if ctx.invoked_subcommand == None: await ctx.send("Error, this command requires at least 1 argument.")

    @emoji.command()
    async def list(self, ctx):
        """Retrieves a list about current guilds emojis"""
        embed = discord.Embed(colour=0xf2c203, title=f"{ctx.guild.name}'s Custom Emojis List")
        emojis = ""
        if len(ctx.guild.emojis)==0: return await ctx.send("Error, this guild doesn't have any emoji.")
        for index, emoji in enumerate(ctx.guild.emojis):
            if len(emojis) >= 1000:
                embed.set_footer(text=f"...and other {len(ctx.guild.emojis) - index} custom emojis (too many to show).")
                break
            emojis += str(emoji) + " "
        embed.add_field(name="Emojis", value=f"{emojis}")
        await ctx.send(embed=embed)

    @emoji.command()
    async def info(self, ctx):
        pass

    @emoji.command()
    async def enlarge(sellf, ctx):
        pass

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
        """Shows info about the mentioned user"""
        member = ctx.author if not member else member
        embed = discord.Embed(colour=0xf2c203)
        created = (member.created_at).strftime("%d %B, %Y")
        joined = (member.joined_at).strftime("%d %B, %Y")
        embed.set_thumbnail(url=f"{member.avatar_url}")
        embed.add_field(name=f"**General Info**", value=f"{emote} **Full name:** {member.name}#{member.discriminator}\n{emote} **User ID:** {member.id}\n{emote} **Nickname:** {member.display_name if member.display_name != member.name else 'None'}\n{emote} **Roles:** {int(len(member.roles))-1}\n{emote} **Activity:** {member.activities[0] if member.activities else 'None'}\n{emote} **Joined Server:** {joined} ({cogs._utils.human_timedelta(member.joined_at)} ago)\n{emote} **User Created:** {created} ({cogs._utils.human_timedelta(member.created_at)} ago)\n{emote} **Bot:** {'<:check:787008166327615509>' if member.bot else '<:cross1:787008036882350100>'}\n{emote} **Avatar url:** [click here]({member.avatar_url})", inline=False)
        embed.add_field(name=f"**Status**", value=f"{cogs._utils.check_status(member, 2)} | \U0001f4f1 Mobile Status\n{cogs._utils.check_status(member, 3)} | \U0001f5a5 Desktop Status\n{cogs._utils.check_status(member, 1)} | <:noxweb:787015386322960405> Web Status")
        await ctx.send(embed=embed)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def serverinfo(self, ctx):
        """Shows info about current server"""
        try:
            bans = len(await ctx.guild.bans())
        except:
            bans = "No permission."
        created = (ctx.guild.created_at).strftime("%d %B, %Y")
        embed = discord.Embed(colour=0xf2c203)
        embed.set_thumbnail(url=f"{ctx.guild.icon_url}")
        embed.add_field(name=f"**General Info**", value=f"{emote} **Name:** {ctx.guild.name}\n{emote} **Description:** {ctx.guild.description}\n{emote} **ID:** {ctx.guild.id}\n{emote} **Region:** {ctx.guild.region}\n{emote} **Verification Level:** {str(ctx.guild.verification_level).capitalize()}\n{emote} **Upload Limit:** {bytes2human(ctx.guild.filesize_limit)}B\n{emote} **Channels:** {len(ctx.guild.text_channels)} Text | {len(ctx.guild.voice_channels)} Voice\n{emote} **Emojis:** {len(ctx.guild.emojis)}/{ctx.guild.emoji_limit}\n{emote} **Created:** {created} ({cogs._utils.human_timedelta(ctx.guild.created_at)} ago)\n{emote} **Shard ID:** {ctx.guild.shard_id}", inline=False)
        embed.add_field(name=f"**Member Info**", value=f"{emote} **Owner:** {ctx.guild.owner.name}#{ctx.guild.owner.discriminator}\n{emote} **Members:** {len(ctx.guild.members)}\n{emote} **Bans:** {bans}\n{emote} **Roles:** {len(ctx.guild.roles)}", inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Info(bot))