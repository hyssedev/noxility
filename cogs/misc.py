from discord.ext import commands
import asyncio, traceback, discord, inspect, textwrap, importlib, io, os, re, sys, copy, time, subprocess, platform, psutil
from contextlib import redirect_stdout
from psutil._common import bytes2human
import parsedatetime as pdt
from dateutil.relativedelta import relativedelta
from datetime import datetime
import cogs._utils
from cogs.info import emote

class Misc (commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def channelinfo(self, ctx):
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
        embed.add_field(name=f"**General Info**", value=f"{emote} **Full name:** {member.name}#{member.discriminator}\n{emote} **User ID:** {member.id}\n{emote} **Nickname:** {member.display_name if member.display_name != member.name else 'None'}\n{emote} **Activity:** {member.activities[0] if member.activities else 'None'}\n{emote} **Joined Server:** {joined} ({cogs._utils.human_timedelta(member.joined_at)} ago)\n{emote} **User Created:** {created} ({cogs._utils.human_timedelta(member.created_at)} ago)\n{emote} **Bot:** {'<:check:787008166327615509>' if member.bot else '<:cross1:787008036882350100>'}\n{emote} **Avatar url:** [click here]({member.avatar_url})", inline=False)
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

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def roleinfo(self, ctx, role: discord.Role):
        created = (role.created_at).strftime("%d %B, %Y, %H:%M")
        owned_by = len(role.members)
        embed = discord.Embed(colour=role.colour)
        embed.add_field(name=f"**User**", value=f"{emote} **Mention:** {role.mention}\n{emote} **ID:** {role.id}\n{emote} **Owned by:** {owned_by} member{'s' if owned_by > 1 else ''}\n{emote} **Created:** {created}\n{emote} **Position:** {role.position}\n{emote} **Hoisted:** {'<:noxcheck:787008166327615509>' if role.hoist else '<:noxcross1:787008036882350100>'}\n{emote} **Mentionable:** {'<:noxcheck:787008166327615509>' if role.mentionable else '<:noxcross1:787008036882350100>'}\n{emote} **Managed:** {'<:noxcheck:787008166327615509>' if role.managed else '<:noxcross1:787008036882350100>'}", inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Misc(bot))