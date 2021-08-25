from discord.ext import commands
from main import main_db
from config import hypixel_api_key
from Bot.utils.UserManagement.guild import *
from Bot.utils.UserManagement.user import *
import discord
import requests
mojang_collection = main_db["mojang"]
users = main_db["users_test"]
verified_role_id = 686200195498770452


class link(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def verify(self, ctx, username):
        if users.find_one({"id": ctx.author.id}):
            await ctx.send(
                f"You're already verified to the account `{users.find_one({'id': ctx.author.id})['uuid']}`")
        else:
            try:
                mojang = requests.get(
                    f'https://api.mojang.com/users/profiles/minecraft/{username}?').json()
            except:
                await ctx.send(
                    f"The name you provided is not valid. Are you sure this is the correct name? `{username}`")
            else:
                player = requests.get(
                    f"https://api.hypixel.net/player?key={hypixel_api_key}&uuid={mojang['id']}").json()
                try:
                    discord_account = player["player"]["socialMedia"]["links"]["DISCORD"]
                except:
                    await ctx.send("You need to link your Discord account to Hypixel!\nhttps://imgur.com/2ZRQzEC.gif")
                    return
                if str(ctx.message.author) != discord_account:
                    await ctx.send(f"Your accounts don't match!\n\nYour Account: {str(ctx.message.author)}\n\
    Linked Account: {player['player']['socialMedia']['links']['DISCORD']}")
                elif str(ctx.message.author) == player["player"]["socialMedia"]["links"]["DISCORD"]:
                    await ctx.author.add_roles(ctx.guild.get_role(verified_role_id))
                    users.insert_one({"id": ctx.author.id, "uuid": mojang["id"]})
                    guild_data = requests.get(
                        f'https://api.hypixel.net/guild?key={hypixel_api_key}&player={mojang["id"]}').json()
                    if guild_data["guild"] is None:
                        await ctx.send("Successfully verified! A guild couldn't be found for you, so you didn't get "
                                       "any guild roles.")
                        return

                    try:
                        tag = guild_data["guild"]["tag"]
                    except:
                        tag = None

                    mojang_collection.insert_one({"uuid": mojang["id"], "username": mojang["name"], "tag": tag})
                    member = get_guild_member(guild_data, mojang["id"])
                    if member is None:
                        await ctx.author.add_roles(ctx.guild.get_role(verified_role_id))
                        users.update_one({"id": ctx.author.id}, {"$set": {"guildPosition": None}})

                    elif check_officer_list(member["rank"].lower()) is True:
                        await ctx.author.add_roles(ctx.guild.get_role(officer_role_id))
                        users.update_one({"id": ctx.author.id}, {"$set": {"guildPosition": "officer"}})
                        await ctx.author.add_roles(ctx.guild.get_role(officer_role_id))

                    elif member["rank"] == "GUILDMASTER":
                        await ctx.author.add_roles(ctx.guild.get_role(officer_role_id),
                                                   ctx.guild.get_role(guildmaster_role_id))
                        users.update_one({"id": ctx.author.id}, {"$set": {"guildPosition": "guildmaster"}})

                    await ctx.author.edit(nick=format_nickname(guild_data, mojang["name"]))
                    await ctx.send("Successfully verified!")


def setup(bot):
    bot.add_cog(link(bot))
