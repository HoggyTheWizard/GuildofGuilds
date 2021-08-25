from discord.ext import commands, tasks
from config import hypixel_api_key
from main import main_db
import discord
import requests
import random
user_data = main_db["users"]
mojang = main_db["mojang"]


class mojang_sync(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # self.mojang_sync.start()

    @commands.command()
    async def yes(self, ctx):
        guild = self.bot.get_guild(473952725063696385)
        print(type(guild))
        the_number = random.randint(1, 421)
        print(the_number)
        count = 0
        for member in guild.members:
            print(member)
            if count == the_number:
                print("triggered this")
                await ctx.send(member.avatar_url)
                return
            else:
                count += 1
                print(count)
                continue
        await ctx.send("Done")

    @tasks.loop(minutes=60)
    async def mojang_sync(self):
        for doc in mojang.find({}):
            try:
                mojang_data = requests.get(f"https://sessionserver.mojang.com/session/minecraft/profile/{doc['uuid']}").json()
            except Exception as e:
                print(f"**Error**: {e}")
                continue
            if doc["id"] != mojang_data["username"]:
                mojang.update_one({"id": doc["id"]}, {"$set": {"username": mojang_data["name"]}})
                print(f"Username Update: Successfully updated {doc['uuid']} ({doc['username']} -> {mojang_data['name']})")

            try:
                guild = requests.get(
                    f'https://api.hypixel.net/guild?key={hypixel_api_key}&player={mojang["id"]}').json()
            except:
                print(f"Couldn't find a guild for {doc['uuid']}")
                continue

            if doc["tag"] is None:
                mojang.update_one({"id": doc["id"]}, {"$set": {"tag": guild["guild"]["tag"]}})
                print(f"Tag Update: Successfully inserted a tag for {doc['uuid']} ({guild['guild']['tag']})")

            elif doc["tag"] != guild["guild"]["tag"]:
                mojang.update_one({"id": doc["id"]}, {"$set": {"tag": guild["guild"]["tag"]}})
                print(f"Tag Update: Successfully updated a tag for {doc['uuid']} ({doc['tag']} -> {guild['guild']['tag']})")
            else:
                continue
    print("Done!")

    @mojang_sync.before_loop
    async def before_printer(self):
        print("Queueing Mojang Sync...")
        await self.bot.wait_until_ready()


def setup(bot):
    bot.add_cog(mojang_sync(bot))
