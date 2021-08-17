from discord.ext import commands
from GuildOfGuilds.main import main_db
users = main_db["users"]
settings = main_db["settings"]


class CommandEnabledCheck(commands.CommandError):
    pass


def commands_enabled():
    def predicate(ctx):
        status = settings.find_one({"id": "status"})["commandsEnabled"]
        if status is True:
            raise CommandEnabledCheck("Commands are currently disabled!")
        else:
            return True
    return commands.check(predicate)
