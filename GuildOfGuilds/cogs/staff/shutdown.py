from discord.ext import commands
from GuildOfGuilds.utils.staff.staff_checks import dev_check
from GuildOfGuilds.main import main_db
from pathlib import Path
from GuildOfGuilds.config import prefixes
users = main_db["users"]
blacklisted_files = ["shutdown", "start", "reload"]


class shutdown(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def shutdown(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send("Available Subcommands:\n"
                           f"{prefixes[0]}shutdown all - Shuts off all files\n"
                           f"{prefixes[0]}shutdown folder <folder_name> - Shuts off all files in a specified folder.\n"
                           f"{prefixes[0]}shutdown folders - Displays a list of the bot's folders.")

    @shutdown.command()
    async def all(self, ctx):
        if dev_check(users, ctx.author.id) is False :
            await ctx.send("This command is for developers only!")
        else:
            count = 0
            for ext in Path().glob("bot/cogs/*/*.py"):
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
    async def folders(self, ctx):
        if dev_check(users, ctx.author.id) is False:
            await ctx.send("This command is for developers only!")
        else:
            string = "Folders:\n"
            for folder in Path().glob(f"bot/cogs/*"):
                try:
                    folder_name = f"{list(folder.parts)[2]}\n"
                    string += folder_name
                except:
                    print(f"{folder} was unable to be added to the string.")
                    continue
            await ctx.send(string)

    @shutdown.command()
    async def folder(self, ctx, folder) :
        if dev_check(users, ctx.author.id) is False :
            await ctx.send("This command is for developers only!")
        else:
            count = 0
            for extension in Path().glob(f"bot/cogs/{folder}/*.py"):
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
