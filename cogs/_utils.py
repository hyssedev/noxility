import json, discord, asyncio, datetime, os
from pathlib import Path
from discord.ext import commands
from discord.ext.buttons import Paginator
from dateutil.relativedelta import relativedelta

emote = "<:noxilityarrow:786985788893560923>"

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
        # if len([g for g in ctx.bot.guilds if g.get_member(member)]) == 0: return
        if member == ctx.author: return await ctx.send(f"Error, you can't do this to yourself.")
        if member.id == ctx.bot.user.id: return await ctx.send("Error, I can't do this to myself.")
        # Check if user bypasses
        if ctx.author.id == ctx.guild.owner.id: return False
        if member.id == bot.owner_id: return await ctx.send("Error, I cannot do this to my developer.")
        # Now permission check
        elif member.id == ctx.guild.owner.id or ctx.author.top_role == member.top_role or ctx.author.top_role < member.top_role:
            return await ctx.send(f"Error, you can't do this because of role hierarchy.")
    except Exception:
        pass

def can_execute_action(ctx, user, target):
    return user.id == ctx.bot.owner_id or \
           user == ctx.guild.owner or \
           user.top_role > target.top_role

async def get_or_fetch_member(self, guild, member_id):
    member = guild.get_member(member_id)
    if member is not None:
        return member

    shard = self.get_shard(guild.shard_id)
    if shard.is_ws_ratelimited():
        try:
            member = await guild.fetch_member(member_id)
        except discord.HTTPException:
            return None

    members = await guild.query_members(limit=1, user_ids=[member_id], cache=True)
    if not members:
        return None
    return members[0]

class MemberID(commands.Converter):
    async def convert(self, ctx, argument):
        try:
            m = await commands.MemberConverter().convert(ctx, argument)
        except commands.BadArgument:
            try:
                member_id = int(argument, base=10)
            except ValueError:
                raise commands.BadArgument(f"{argument} is not a valid member or member ID.") from None
            else:
                m = await get_or_fetch_member(ctx.guild, member_id)
                if m is None:
                    # hackban case
                    return type('_Hackban', (), {'id': member_id, '__str__': lambda s: f'Member ID {s.id}'})()

        if not can_execute_action(ctx, ctx.author, m):
            raise commands.BadArgument('You cannot do this action on this user due to role hierarchy.')
        return m

class Pag(Paginator):
    async def teardown(self):
        try:
            await self.page.clear_reactions()
        except discord.HTTPException:
            pass


class EmbedHelpCommand(commands.HelpCommand):
    """This is an example of a HelpCommand that utilizes embeds.
    It's pretty basic but it lacks some nuances that people might expect.
    1. It breaks if you have more than 25 cogs or more than 25 subcommands. (Most people don't reach this)
    2. It doesn't DM users. To do this, you have to override `get_destination`. It's simple.
    Other than those two things this is a basic skeleton to get you started. It should
    be simple to modify if you desire some other behaviour.
    
    To use this, pass it to the bot constructor e.g.:
       
    bot = commands.Bot(help_command=EmbedHelpCommand())
    """
    # Set the embed colour here

    def __init__(self):
        super().__init__(command_attrs={'help': 'Shows help about commands etc.', 'cooldown': commands.Cooldown(1,10,commands.BucketType.user), 'hidden': True})

    COLOUR = 0xf2c203
    
    def get_ending_note(self):
        return 'Use {0}{1} [command] for more info on a command.'.format(self.clean_prefix, self.invoked_with)

    def get_command_signature(self, command):
        aliases = "|".join(command.aliases)
        cmd_invoke = f"[{command.name}|{aliases}]" if command.aliases else command.name
        full_invoke = command.qualified_name.replace(command.name, "")

        signature = f"{self.clean_prefix}{full_invoke}{cmd_invoke} {command.signature}"
        return signature

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title='Bot Commands', colour=self.COLOUR)
        description = self.context.bot.description
        if description:
            embed.description = f"{description} It currently has {len([i for i in self.context.bot.walk_commands()])} commands.\n```[] = optional argument\n<> = required argument\nDo not write these when using commands.\nIf there is any space in a cog name, please type '_' instead of it.\nType nox help [command | module] for more help on a command or module.```\n"

        for cog, commands in mapping.items():
            name = 'No Category' if cog is None else str(cog.qualified_name).replace("_", " ")
            if name != 'No Category':
                filtered = await self.filter_commands(commands, sort=True)
                if filtered:
                    # value = '\u2002'.join(c.name for c in commands if c.name != "help")
                    value = ', '.join(c.name for c in commands)
                    if cog and cog.description:
                        value = '{0}\n{1}'.format(cog.description, value)

                    embed.add_field(name=name, value=f"```{value}```", inline=False)

        embed.set_footer(text=self.get_ending_note())
        await self.get_destination().send(embed=embed)

    async def send_cog_help(self, cog):
        embed = discord.Embed(title=f'{cog.qualified_name.replace("_", " ")} Commands', colour=self.COLOUR)
        if cog.description:
            embed.description = cog.description

        filtered = await self.filter_commands(cog.get_commands(), sort=True)
        for command in filtered:
            embed.add_field(name=self.get_command_signature(command), value=command.short_doc or '...', inline=False)

        embed.set_footer(text=self.get_ending_note())
        await self.get_destination().send(embed=embed)

    async def send_group_help(self, group):
        embed = discord.Embed(title=self.get_command_signature(group), colour=self.COLOUR)
        if group.help:
            embed.description = group.help

        if isinstance(group, commands.Group):
            filtered = await self.filter_commands(group.commands, sort=True)
            for command in filtered:
                embed.add_field(name=self.get_command_signature(command), value=command.short_doc or '...', inline=False)

        embed.set_footer(text=self.get_ending_note())
        await self.get_destination().send(embed=embed)

    # This makes it so it uses the function above
    # Less work for us to do since they're both similar.
    # If you want to make regular command help look different then override it
    send_command_help = send_group_help

# uptime

class plural:
    def __init__(self, value):
        self.value = value
    def __format__(self, format_spec):
        v = self.value
        singular, sep, plural = format_spec.partition('|')
        plural = plural or f'{singular}s'
        if abs(v) != 1:
            return f'{v} {plural}'
        return f'{v} {singular}'

def human_join(seq, delim=', ', final='or'):
    size = len(seq)
    if size == 0:
        return ''

    if size == 1:
        return seq[0]

    if size == 2:
        return f'{seq[0]} {final} {seq[1]}'

    return delim.join(seq[:-1]) + f' {final} {seq[-1]}'

def human_timedelta(dt, *, source=None, accuracy=3, brief=False, suffix=False):
    now = source or datetime.datetime.utcnow()
    # Microsecond free zone
    now = now.replace(microsecond=0)
    dt = dt.replace(microsecond=0)

    # This implementation uses relativedelta instead of the much more obvious
    # divmod approach with seconds because the seconds approach is not entirely
    # accurate once you go over 1 week in terms of accuracy since you have to
    # hardcode a month as 30 or 31 days.
    # A query like "11 months" can be interpreted as "!1 months and 6 days"
    if dt > now:
        delta = relativedelta(dt, now)
        suffix = ''
    else:
        delta = relativedelta(now, dt)
        suffix = ' ago' if suffix else ''

    attrs = [
        ('year', 'y'),
        ('month', 'mo'),
        ('day', 'd'),
        ('hour', 'h'),
        ('minute', 'm'),
        ('second', 's'),
    ]

    output = []
    for attr, brief_attr in attrs:
        elem = getattr(delta, attr + 's')
        if not elem:
            continue

        if attr == 'day':
            weeks = delta.weeks
            if weeks:
                elem -= weeks * 7
                if not brief:
                    output.append(format(plural(weeks), 'week'))
                else:
                    output.append(f'{weeks}w')

        if elem <= 0:
            continue

        if brief:
            output.append(f'{elem}{brief_attr}')
        else:
            output.append(format(plural(elem), attr))

    if accuracy is not None:
        output = output[:accuracy]

    if len(output) == 0:
        return 'now'
    else:
        if not brief:
            return human_join(output, final='and') + suffix
        else:
            return ' '.join(output) + suffix

def check_status(member, status):
    online = "<:noxonline:787010419071778866>"
    offline = "<:noxoff:787010550865330187>"
    dnd = "<:noxdnd:787010502017548369>"
    idle = "<:noxidle:787010460980609084>"
    if status == 1: check = member.web_status
    elif status == 2: check = member.mobile_status
    elif status == 3: check = member.desktop_status
    
    if check == discord.Status.online: return online
    if check == discord.Status.offline: return offline
    if check == discord.Status.idle: return idle
    if check == discord.Status.dnd: return dnd

def plural_check(smth):
    return 's' if smth > 1 else ''

def countlines(start, lines=0, begin_start=None):
    for thing in os.listdir(start):
        thing = os.path.join(start, thing)
        if os.path.isfile(thing):
            if thing.endswith('.py'):
                with open(thing, 'r') as f:
                    newlines = f.readlines()
                    newlines = len(newlines)
                    lines += newlines

    for thing in os.listdir(start):
        thing = os.path.join(start, thing)
        if os.path.isdir(thing):
            lines = countlines(thing, lines, begin_start=start)

    return lines