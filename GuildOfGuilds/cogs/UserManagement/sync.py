from discord.ext import commands, tasks
from GuildOfGuilds.config import hypixel_api_key, guild_id
from GuildOfGuilds.utils.UserManagement.sync import *
from GuildOfGuilds.main import main_db
from GuildOfGuilds.utils.UserManagement.user import *
from GuildOfGuilds.utils.UserManagement.guild import get_guild_member, check_officer_list
import discord
import asyncio
import requests
users = main_db["users"]
mojang = main_db["mojang"]


class user_sync(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # self.user_sync.start()

    @tasks.loop(minutes=30)
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

            elif member.nick != f"{data['username']} [{data['tag']}]":
                await member.edit(nick=format_nickname_from_db(data["tag"], data["username"]))

            if user["guildPosition"] is None:
                continue
            else:
                guild_data = requests.get(
                    f'https://api.hypixel.net/guild?key={hypixel_api_key}&player={mojang["id"]}').json()
                gm = get_guild_member(guild_data, mojang["id"])
                if gm["rank"] != user["guildPosition"]:
                    if user["guildPosition"] == "officer":
                        await member.remove_roles(guild.get_role(get_guild_role_from_db().get("guildmaster")))
                    elif user["guildPosition"] == "guildmaster":
                        await member.remove_roles(guild.get_role(get_guild_role_from_db().get("guildmaster")))

                    if gm["rank"] == "GUILDMASTER":
                        await member.add_roles(get_guild_role_from_db().get("guildmaster"), get_guild_role_from_db().get("officer"))
                        users.update_one({"id": member.id}, {"$set": {"guildPosition": "guildmaster"}})

                    elif check_officer_list(gm["rank"].lower()) is True:
                        if user["guildPosition"] == "guildmaster":
                            await member.remove_roles(get_guild_role_from_db().get("guildmaster"))

                        await member.add_roles(get_guild_role_from_db().get("officer"))
                        users.update_one({"id": member.id}, {"$set": {"guildPosition": "guildmaster"}})

                    else:
                        if user["guildPosition"] == "guildmaster":
                            await member.add_roles(get_guild_role_from_db().get("guildmaster"),
                                                   get_guild_role_from_db().get("officer"))
                        await member.remove_roles(get_guild_role_from_db().get(user["guildPosition"]))
                        users.update_one({"id": member.id}, {"$set": {"guildPosition": None}})
        await asyncio.sleep(5)
    print("Finished Sync Task")

    @user_sync.before_loop
    async def before_printer(self):
        print("Queueing User Sync...")
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(user_sync(bot))
