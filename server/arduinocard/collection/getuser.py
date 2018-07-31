from collection.models import Basic_info



def getuser(user_ID):
    this_user = Basic_info.objects.filter(idnumber=user_ID).order_by("id")
    if this_user.exists():
        for users in this_user:
            return users
    else:
        return None

