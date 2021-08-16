from discord.ext import commands
from GuildOfGuilds.utils.staff.staff_checks import *
from GuildOfGuilds.main import main_db
import discord
import requests
users = main_db["users"]


class link(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @is_staff()
    async def link(self, ctx, member: discord.Member, username):
        try:
            mojang = requests.get(f'https://api.mojang.com/users/profiles/minecraft/{username}?').json()
            if users.find_one({"id": member.id}) is None:
                users.insert_one({"id": member.id, "uuid": mojang["id"]})
                await ctx.send(f"Successfully linked {str(member)} to {mojang['name']} ({mojang['id']})")
            else:
                await ctx.send("This user is already linked!")
        except Exception as e:
            print("Error")
            await ctx.send(f"*Error**: {e}")

    @commands.command()
    @is_staff()
    async def unlink(self, ctx, member: discord.Member):
            try:
                users.delete_one({"id": member.id})
                await ctx.send(f"Successfully deleted data for {str(member)} ({member.id})")
            except Exception as e:
                await ctx.send(f"*Error**: {e}")


def setup(bot):
    bot.add_cog(link(bot))
