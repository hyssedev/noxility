from discord.ext import commands
import asyncio, traceback, discord, inspect, textwrap, importlib, io, os, re, sys, copy, time, subprocess
from contextlib import redirect_stdout
import cogs._utils

class OwnerOnly (commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None
    
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
        """Evaluates a code"""
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

    @commands.command(aliases=['disconnect', 'close', 'stopbot'])
    @commands.is_owner()
    async def logout(self, ctx):
        await ctx.send(f"Noxility logging out.")
        await self.bot.logout()

    @commands.command()
    async def echo(self, ctx, *, message=None):
        message = message or "What do you want me to repeat?"
        await ctx.message.delete()
        await ctx.send(message)

    @commands.group(invoke_without_command=False)
    @commands.is_owner()
    async def blacklist(self, ctx):
        pass

    @blacklist.command()
    async def add(self, ctx, user: discord.Member=None):
        user = ctx.author if not user else user
        if user.id == ctx.author.id: return await ctx.send("Error: You can't blacklist yourself.")
        print(type(self.bot.blacklisted_users))
        self.bot.blacklisted_users.append(user.id)
        data = cogs._utils.read_json("blacklist")
        data["blacklistedUsers"].append(user.id)
        cogs._utils.write_json(data, "blacklist")
        await ctx.send(f"Blacklisted {user.name}.")

    @blacklist.command()
    async def remove(self, ctx, user: discord.Member=None):
        user = ctx.author if not user else user
        if user.id == ctx.author.id: return await ctx.send("Error: You can't whitelist yourself.")
        self.bot.blacklisted_users.remove(user.id)
        data = cogs._utils.read_json("blacklist")
        data["blacklistedUsers"].remove(user.id)
        cogs._utils.write_json(data, "blacklist")
        await ctx.send(f"Unblacklisted {user.name}.")

def setup(bot):
    bot.add_cog(OwnerOnly(bot))