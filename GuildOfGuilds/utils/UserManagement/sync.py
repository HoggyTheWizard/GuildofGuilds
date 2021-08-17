from discord.ext import commands
from GuildOfGuilds.utils.UserManagement.guild import officer_role_id, guildmaster_role_id


class SyncUtils(commands.CommandError):
    pass


def get_guild_role_from_db():
    try:
        dictionary = {
            None: None,
            "officer": officer_role_id,
            "guildmaster": guildmaster_role_id
        }
        return dictionary
    except:
        raise SyncUtils("Invalid Position Provided")
