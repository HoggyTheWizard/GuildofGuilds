def format_nickname(guild, username):
    try:
        suffix = guild["guild"]["tag"]
    except:
        suffix = None

    if suffix is not None:
        return f"{username} [{suffix}]"
    else:
        return username
