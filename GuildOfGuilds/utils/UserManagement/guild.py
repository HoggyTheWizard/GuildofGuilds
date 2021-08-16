officer_aliases = ["officer", "owner", "co-owner", "coowner", "leader"]
guildmaster_role_id = 588038218264477756
officer_role_id = 635429831672070155
verified_role_id = 0


def get_guild_member(guild, uuid):
    try:
        for member in guild["guild"]["members"]:
            if member["uuid"] == uuid:
                return member
    except:
        return None


def check_officer_list(name):
    try:
        if name in officer_aliases:
            return True
        else:
            return False
    except Exception as e:
        print(f"**Error**: {e}")
        return False


def guild_rank_to_role():
    try:

        rank_to_role = {
            'Member': member_role_id,
            'GuildMVP': gmvp_role_id,
            'GuildElite': gelite_role_id,
            'Event Winner': eventwinner_role_id,
            'Staff Team': staff
        }
        return rank_to_role
    except:
        print('triggered except')
        return 'fsdgsgsfgsdfg'