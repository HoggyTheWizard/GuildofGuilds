from discord.ext import commands
from GuildOfGuilds.utils.staff.staff_checks import *
from GuildOfGuilds.main import main_db
from pathlib import Path
from GuildOfGuilds.config import prefixes
users = main_db["users"]
blacklisted_files = ["shutdown", "start", "reload"]


class devtools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def reload(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Available Subcommands:\n"
                           f"{prefixes[0]}reload all - Reloads all files\n"
                           f"{prefixes[0]}reload folder <folder_name> - Reloads all cogs in the specified folder.\n"
                           f"{prefixes[0]}reload folders - Displays a list of the bot's folders.")

    @reload.command()
    @is_dev()
    async def all(self, ctx):
        for ext in Path().glob("bot/cogs/*/*.py"):
            try:
                self.bot.unload_extension(".".join(part for part in ext.parts)[:-len(ext.suffix)])
            except Exception:
                print(f"Could not load extension {ext}")
        count = 0
        for ext in Path().glob("bot/cogs/*/*.py"):
            try:
                self.bot.load_extension(".".join(part for part in ext.parts)[:-len(ext.suffix)])
                count += 1
            except Exception:
                print(f"Could not load extension {ext}")
        await ctx.send(f"Success! Files Reloaded: {count}")

    @reload.command()
    @is_dev()
    async def folders(self, ctx):
        string = "Folders:\n"
        for folder in Path().glob(f"bot/cogs/*"):
            try:
                folder_name = f"{list(folder.parts)[2]}\n"
                string += folder_name
            except:
                print(f"{folder} was unable to be added to the string.")
                continue
        await ctx.send(string)

    @reload.command()
    @is_dev()
    async def folder(self, ctx, folder):
        for extension in Path().glob(f"bot/cogs/{folder}/*.py"):
            try:
                self.bot.unload_extension(".".join(part for part in extension.parts)[:-len(extension.suffix)])
            except:
                print(f"Could not load extension {extension}")

        count = 0
        for extension in Path().glob(f"bot/cogs/{folder}/*.py"):
            try:
                self.bot.load_extension(".".join(part for part in extension.parts)[:-len(extension.suffix)])
                count += 1
            except:
                print(f"Could not load extension {extension}")
        await ctx.send(f"Success! Files Reloaded: {count}")


def setup(bot):
    bot.add_cog(devtools(bot))
