from discord.ext import commands, tasks
import asyncio, traceback, discord, inspect, textwrap, importlib, io, os, re, sys, copy, time, subprocess
from contextlib import redirect_stdout
 # pylint: disable=no-member
class Developer (commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None
        self.activity.start()

    def cog_unload(self):
        self.activity.cancel()
    
    def cleanup_code(self, content):
        """Automatically removes code blocks from the code."""
        # remove ```py\n```
        if content.startswith('```') and content.endswith('```'):
            return '\n'.join(content.split('\n')[1:-1])

        # remove `foo`
        return content.strip('` \n')

    @commands.command(name='eval')
    @commands.is_owner()
    async def _eval(self, ctx, *, body: str):
        """Evaluates code"""
        env = {
            'bot': self.bot,
            'ctx': ctx,
            'channel': ctx.channel,
            'author': ctx.author,
            'guild': ctx.guild,
            'message': ctx.message,
            '_': self._last_result
        }

        env.update(globals())

        body = self.cleanup_code(body)
        stdout = io.StringIO()

        to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

        try:
            exec(to_compile, env)
        except Exception as e:
            return await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')

        func = env['func']
        try:
            with redirect_stdout(stdout):
                ret = await func()
        except Exception as e:
            value = stdout.getvalue()
            await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
        else:
            value = stdout.getvalue()
            try:
                await ctx.message.add_reaction('\u2705')
            except:
                pass

            if ret is None:
                if value:
                    await ctx.send(f'```py\n{value}\n```')
            else:
                self._last_result = ret
                await ctx.send(f'```py\n{value}{ret}\n```')

    @commands.command()
    @commands.is_owner()
    async def logout(self, ctx):
        """Logs the bot out."""
        await ctx.send(f"Noxility logging out.")
        await self.bot.logout()

    @commands.command()
    @commands.is_owner()
    async def echo(self, ctx, *, message):
        """Repeats your message."""
        message = message or "What do you want me to repeat?"
        await ctx.message.delete()
        await ctx.send(message)

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx, cog=None):
        """Reloads specified cog."""
        if not cog:
            # No cog, means we reload all cogs
            async with ctx.typing():
                embed = discord.Embed(title="Reloading...", color=0xf2c203, timestamp=ctx.message.created_at)
                for ext in os.listdir("./cogs/"):
                    if ext.endswith(".py") and not ext.startswith("_"):
                        try:
                            self.bot.unload_extension(f"cogs.{ext[:-3]}")
                            self.bot.load_extension(f"cogs.{ext[:-3]}")
                            embed.add_field(name=f"Reloaded: `{ext[:-3]}`", value='\uFEFF', inline=False)
                        except Exception as e:
                            embed.add_field(name=f"Failed to reload: `{ext[:-3]}`", value=e, inline=False)
                        await asyncio.sleep(0.5)
                await ctx.send(embed=embed)
        else:
            # reload the specific cog
            embed = discord.Embed(title="Reloading...", color=0xf2c203, timestamp=ctx.message.created_at)
            ext = f"{cog}.py"
            if not os.path.exists(f"./cogs/{ext}"):
                # if the file does not exist
                embed.add_field(name=f"Failed to reload: `{ext[:-3]}`", value="This cog does not exist.", inline=False)

            elif ext.endswith(".py") and not ext.startswith("_"):
                try:
                    self.bot.unload_extension(f"cogs.{ext[:-3]}")
                    self.bot.load_extension(f"cogs.{ext[:-3]}")
                    embed.add_field(name=f"Reloaded: `{ext[:-3]}`", value='\uFEFF', inline=False)
                except Exception:
                    desired_trace = traceback.format_exc()
                    embed.add_field(name=f"Failed to reload: `{ext[:-3]}`", value=desired_trace, inline=False)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def unload(self, ctx, cog=None):
        """Unloads specified cog."""
        cogs = []
        for cogg in os.listdir("./cogs/"):
            if cogg.endswith(".py") and not cogg.startswith("_"):
                cogs.append(cogg)
        if cog is None: await ctx.send(f"Please specify which cog to unload. Available cogs: {', '.join(cogs)}.")
        embed = discord.Embed(title="Unloading...", color=0xf2c203, timestamp=ctx.message.created_at)
        ext = f"{cog}.py"
        if not os.path.exists(f"./cogs/{ext}"):
            # if the file does not exist
            embed.add_field(name=f"Failed to unload: `{ext[:-3]}`", value="This cog does not exist.", inline=False)

        elif ext.endswith(".py") and not ext.startswith("_"):
            try:
                self.bot.unload_extension(f"cogs.{ext[:-3]}")
                embed.add_field(name=f"Unloaded: `{ext[:-3]}`", value='\uFEFF', inline=False)
            except Exception:
                desired_trace = traceback.format_exc()
                embed.add_field(name=f"Failed to unload: `{ext[:-3]}`", value=desired_trace, inline=False)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def load(self, ctx, cog=None):
        """Loads specified cog."""
        cogs = []
        for cogg in os.listdir("./cogs/"):
            if cogg.endswith(".py") and not cogg.startswith("_"):
                cogs.append(cogg)
        if cog is None: await ctx.send(f"Please specify which cog to load. Available cogs: {', '.join(cogs)}.")
        embed = discord.Embed(title="Loading...", color=0xf2c203, timestamp=ctx.message.created_at)
        ext = f"{cog}.py"
        if not os.path.exists(f"./cogs/{ext}"):
            # if the file does not exist
            embed.add_field(name=f"Failed to load: `{ext[:-3]}`", value="This cog does not exist.", inline=False)

        elif ext.endswith(".py") and not ext.startswith("_"):
            try:
                self.bot.load_extension(f"cogs.{ext[:-3]}")
                embed.add_field(name=f"Loaded: `{ext[:-3]}`", value='\uFEFF', inline=False)
            except Exception:
                desired_trace = traceback.format_exc()
                embed.add_field(name=f"Failed to load: `{ext[:-3]}`", value=desired_trace, inline=False)

    @commands.group(invoke_without_command=True, name="command")
    @commands.is_owner()
    async def _command(self, ctx):
        if ctx.invoked_subcommand == None: return

    @_command.command()
    @commands.is_owner()
    async def disable(self, ctx, command=None):
        if command is None: await ctx.send(f"Please specify which command to disable.")
        embed = discord.Embed(title="Command disabled", color=0xf2c203, timestamp=ctx.message.created_at)

        try:
            self.bot.get_command(f"{command}").enabled=False
            embed.add_field(name=f"Disabled: `{command}`", value='\uFEFF', inline=False)
        except:
            desired_trace = traceback.format_exc()
            embed.add_field(name=f"Failed to disable: `{command}`", value=desired_trace, inline=False)

    # ----- updating activity every hour ------
    @tasks.loop(minutes=60)
    async def activity(self):
        await self.bot.change_presence(activity=discord.Game(name=f"nox help | {str(len(self.bot.guilds))} guilds"))

    @activity.after_loop
    async def post_activity(self):
        if self.activity.failed():
            import traceback
            error = self.activity.get_task().exception()
            traceback.print_exception(type(error), error, error.__traceback__)

    @activity.before_loop
    async def before_activity(self):
        await self.bot.wait_until_ready()

def setup(bot):
    bot.add_cog(Developer(bot))