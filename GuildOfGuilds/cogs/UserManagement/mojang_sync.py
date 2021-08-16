from discord.ext import commands, tasks
from GuildOfGuilds.config import hypixel_api_key
from GuildOfGuilds.main import main_db
import discord
import requests
user_data = main_db["users"]
mojang = main_db["mojang"]


class mojang_sync(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        #self.mojang_sync.start()

    @tasks.loop(minutes=60)
    async def mojang_sync(self):
        for doc in mojang.find({}):
            try:
                mojang_data = requests.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{doc['uuid']}").json()
            except Exception as e:
                print(f"**Error**: {e}")
                continue
                mojang.insert_one({"uuid": user, "username": username})
                print(f"Successfully inserted {guild_member['uuid']}")
            elif user["username"] != username:
                mojang.update_one({"id": user['id']}, {"$set": {"username": username}})
                print(f"Successfully updated {guild_member['uuid']}")
            else:
                print(f"Skipped {guild_member['uuid']}")
                continue
        print("Done!")

    @mojang_sync.before_loop
    async def before_printer(self):
        print("Queueing Mojang Sync...")
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(mojang_sync(bot))
