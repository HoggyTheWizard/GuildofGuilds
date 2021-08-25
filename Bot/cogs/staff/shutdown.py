from discord.ext import commands
from Bot.utils.staff.staff_checks import *
from main import main_db
from pathlib import Path
from config import prefixes
users = main_db["users"]
blacklisted_files = ["shutdown", "start", "reload"]


class shutdown(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @is_dev()
    async def shutdown(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Available Subcommands:\n"
                           f"{prefixes[0]}shutdown all - Shuts off all files\n"
                           f"{prefixes[0]}shutdown folder <folder_name> - Shuts off all files in a specified folder.\n"
                           f"{prefixes[0]}shutdown folders - Displays a list of the bot's folders.")

    @shutdown.command()
    @is_dev()
    async def all(self, ctx):
        count = 0
        for ext in Path().glob("Bot/cogs/*/*.py"):
            if ext.parts[2] == "Staff":
                if ext.stem in blacklisted_files:
                    continue
            try:
                self.bot.unload_extension(".".join(part for part in ext.parts)[:-len(ext.suffix)])
                count += 1
            except:
                print(f"Could not load extension {ext}")

        await ctx.send(f"Successfully Shut Down: {count} files.")

    @shutdown.command()
    @is_dev()
    async def folders(self, ctx):
        string = "Folders:\n"
        for folder in Path().glob(f"Bot/cogs/*"):
            try:
                folder_name = f"{list(folder.parts)[2]}\n"
                string += folder_name
            except:
                print(f"{folder} was unable to be added to the string.")
                continue
        await ctx.send(string)

    @shutdown.command()
    @is_dev()
    async def folder(self, ctx, folder):
        count = 0
        for extension in Path().glob(f"Bot/cogs/{folder}/*.py"):
            if extension.parts[2] == "Staff":
                if extension.stem in blacklisted_files:
                    continue
            try:
                self.bot.unload_extension(".".join(part for part in extension.parts)[:-len(extension.suffix)])
                count += 1
            except:
                print(f"Could not shut down extension {extension}")

        await ctx.send(f"Success! Shut down {count} cogs in {folder}")


def setup(bot):
    bot.add_cog(shutdown(bot))
