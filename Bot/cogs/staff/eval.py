import discord
from discord.ext import commands
from main import main_db
from config import hoggy_irl_name
users = main_db["user_data"]
from Bot.utils.staff.staff_checks import *
from Bot.utils.staff.eval import *
import io
import contextlib
import textwrap
from traceback import format_exception
import requests


class eval_command(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def mem(self, ctx):
        await ctx.send(ctx.guild.get_member(524755715655467019))

    @commands.command(name="eval", aliases=["exec"])
    @commands.is_owner()
    async def _eval(self, ctx, *, code):
        code = clean_code(code)

        local_variables = {
            "discord": discord,
            "commands": commands,
            "self.bot": self.bot,
            "ctx": ctx,
            "channel": ctx.channel,
            "author": ctx.author,
            "guild": ctx.guild,
            "message": ctx.message,
            "requests": requests,
            "users": users
        }

        stdout = io.StringIO()

        try:
            with contextlib.redirect_stdout(stdout):
                exec(
                    f"async def func():\n{textwrap.indent(code, '    ')}", local_variables,
                )
                color = discord.Color.green()
                obj = await local_variables["func"]()
                result = f"{stdout.getvalue()}"
        except Exception as e:
            color = discord.Color.red()
            result = "".join(format_exception(e, e, e.__traceback__)).replace(hoggy_irl_name, "Hoggy")
        embed = discord.Embed(title="Code Executed", description=f"```py\n{result}\n```", color=color)
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(eval_command(bot))
