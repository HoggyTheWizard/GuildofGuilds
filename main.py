from discord import ActivityType, AllowedMentions
from BotUtilities import BotUtilities
from discord.ext import commands
from config import database_user, database_password, database_name
import logging
import discord
import config
import pymongo

cluster = pymongo.MongoClient(f"mongodb+srv://{database_user}:{database_password}@cluster0.2uexc.mongodb.net/\
{database_name}?retryWrites=true&w=majority")
main_db = cluster['main_data']


logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(levelname)s - %(name)s] %(message)s")
logging.getLogger("discord").setLevel(logging.WARNING)

bot = BotUtilities(commands.when_mentioned_or(*config.prefixes),
                    case_insensitive=True, max_messages=None, intents=discord.Intents.all(), help_command=None)


bot.run(config.token)
