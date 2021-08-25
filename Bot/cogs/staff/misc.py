from discord.ext import commands
from main import main_db
from Bot.utils.staff.staff_checks import *
import discord
users = main_db["users"]
verified_role_id = 686200195498770452


class misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @is_dev()
    async def bypass(self, ctx, target: discord.Member = None):

        if target is None:
            target_self = True
            user_id = ctx.author.id
        else:
            target_self = False
            user_id = target.id

        user = users.find_one({"id": user_id})
        if "bypassEnabled" not in user:
            new_type = True
        elif user["bypassEnabled"] is True:
            new_type = False
        elif user["bypassEnabled"] is False:
            new_type = True
        else:
            new_type = False

        users.update_one({"id": user_id}, {"$set": {"bypassEnabled": new_type}})
        if target_self is True:
            await ctx.send(f"Successfully set bypassEnabled permission to {new_type}")
        elif target_self is False:
            await ctx.send(f"Successfully set bypassEnabled permission to {new_type} for {str(target)}")

    @commands.command()
    @is_dev()
    async def synclock(self, ctx, target: discord.Member = None):

        if target is None:
            target_self = True
            user_id = ctx.author.id
        else:
            target_self = False
            user_id = target.id

        user = users.find_one({"id": user_id})
        if "synclockEnabled" not in user:
            new_type = True
        elif user["synclockEnabled"] is True:
            new_type = False
        elif user["synclockEnabled"] is False:
            new_type = True
        else:
            new_type = False

        users.update_one({"id": user_id}, {"$set": {"synclockEnabled": new_type}})
        if target_self is True:
            await ctx.send(f"Successfully set synclockEnabled permission to {new_type}")
        elif target_self is False:
            await ctx.send(f"Successfully set synclockEnabled permission to {new_type} for {str(target)}")


def setup(bot):
    bot.add_cog(misc(bot))
