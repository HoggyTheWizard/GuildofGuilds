from discord.ext import commands, tasks
from GuildOfGuilds.config import hypixel_api_key, guild_id
from GuildOfGuilds.main import main_db
from GuildOfGuilds.utils.UserManagement.user import *
import discord
import asyncio
import requests
users = main_db["users"]
mojang = main_db["mojang"]


class user_sync(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # self.user_sync.start()

    @tasks.loop(minutes=60)
    async def user_sync(self):
        guild = self.bot.get_guild(guild_id)
        for user in users.find({}):
            try:
                data = mojang.find_one({"uuid": user["uuid"]})
            except None:
                print(f"Warning: {user['id']} does not have a mojang collection document!")
                continue
            try:
                member = guild.get_member(user["id"])
            except:
                print(f"Skipping {user['id']} because they are no longer in the server or their Member object is not "
                      "loading properly.")
                continue

            if member.nick is None:
                if member.name != data["username"]:
                    await member.edit(nick=format_nickname_from_db(data["tag"], data["username"]))


    print("Done!")

    @user_sync.before_loop
    async def before_printer(self):
        print("Queueing User Sync...")
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(user_sync(bot))
