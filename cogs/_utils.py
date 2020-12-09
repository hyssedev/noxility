import json, discord, asyncio
from pathlib import Path
from discord.ext import commands

def get_path():
    """
    A function to get the current path to bot.py
    Returns:
     - cwd (string) : Path to bot.py directory
    """
    cwd = Path(__file__).parents[1]
    cwd = str(cwd)
    return cwd

def read_json(filename):
    """
    A function to read a json file and return the data.
    Params:
     - filename (string) : The name of the file to open
    Returns:
     - data (dict) : A dict of the data in the file
    """
    cwd = get_path()
    with open(cwd+'/config/'+filename+'.json', 'r') as file:
        data = json.load(file)
    return data

def write_json(data, filename):
    """
    A function used to write data to a json file
    Params:
     - data (dict) : The data to write to the file
     - filename (string) : The name of the file to write to
    """
    cwd = get_path()
    with open(cwd+'/config/'+filename+'.json', 'w') as file:
        json.dump(data, file, indent=4)

async def role_hierarchy(ctx, member):
    """ Custom way to check permissions when handling moderation commands """
    try:
        # Self checks
        if member == ctx.author: return await ctx.send(f"You can't do this to yourself")
        if member.id == ctx.bot.user.id: return await ctx.send("I can't do this to myself")
        # Check if user bypasses
        if ctx.author.id == ctx.guild.owner.id: return False
        # Now permission check
        # todo: check if he is trying the command on bot owner
        if member.id == ctx.guild.owner.id or ctx.author.top_role == member.top_role or ctx.author.top_role < member.top_role:
            return await ctx.send(f"You can't do this because of role hierarchy.")
    except Exception:
        pass

class MemberID(commands.Converter):
    async def convert(self, ctx, argument):
        try:
            m = await commands.MemberConverter().convert(ctx, argument)
        except commands.BadArgument:
            try:
                return int(argument, base=10)
            except ValueError:
                raise commands.BadArgument(f"{argument} is not a valid member or member ID.") from None
        else:
            return m