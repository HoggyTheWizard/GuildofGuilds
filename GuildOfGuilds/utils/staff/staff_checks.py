from discord.ext import commands
from GuildOfGuilds.main import main_db
users = main_db["users"]

not_dev_error = "This command is for developers only!"
not_staff_error = "This command is for staff members only!"


class StaffChecks(commands.CommandError):
    pass


def is_dev():
    def predicate(ctx):
        user = users.find_one({"id": ctx.author.id})
        if user is None:
            raise StaffChecks(not_dev_error)
        elif "isDev" not in user:
            raise StaffChecks(not_dev_error)
        elif user["isDev"] is False:
            raise StaffChecks(not_dev_error)
        else:
            return True

    return commands.check(predicate)


def is_staff():
    def predicate(ctx):
        user = users.find_one({"id": ctx.author.id})
        if user is None:
            raise StaffChecks(not_staff_error)
        elif "isDev" not in user:
            raise StaffChecks(not_staff_error)
        elif user["isStaff"] is False:
            raise StaffChecks(not_staff_error)
        else:
            return True

    return commands.check(predicate)
