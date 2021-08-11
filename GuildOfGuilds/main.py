from discord import ActivityType
from discord.ext import commands
from GuildOfGuilds.config import database_user, database_password, database_name
from BotUtilities import BotUtilities
import logging
import discord
from GuildOfGuilds import config
import pymongo

cluster = pymongo.MongoClient(f"mongodb+srv://{database_user}:{database_password}@cluster0.2uexc.mongodb.net/\
{database_name}?retryWrites=true&w=majority")

main_db = cluster["main_data"]
settings = main_db["bot_settings"]


logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(levelname)s - %(name)s] %(message)s")
logging.getLogger("discord").setLevel(logging.WARNING)

bot = BotUtilities(commands.when_mentioned_or(*config.prefixes),
                   case_insensitive=True,
                   activity=discord.Activity(
                    activity=discord.Activity(name=f"{config.prefixes[0]}help", type=ActivityType.listening),
                    max_messages=None, intents=discord.Intents.all(), help_command=None))

bot.run(config.token)
