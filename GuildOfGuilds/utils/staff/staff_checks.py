def dev_check(users, author_id):
    try:
        check = users.find_one({"id": author_id})["isDev"]
        if check is True:
            return True
        else:
            return False
    except:
        return False