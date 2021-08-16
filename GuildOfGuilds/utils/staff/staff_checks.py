def dev_check(users, author_id):
    try:
        if users.find_one({"id": author_id})["isDev"] is True:
            print("true")
            return True
        else:
            return False
    except:
        return False


def staff_check(users, author_id):
    try:
        if users.find_one({"id": author_id})["isStaff"] is True:
            return True
        else:
            return False
    except:
        return False
