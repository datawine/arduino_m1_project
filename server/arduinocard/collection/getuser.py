from collection.models import Basic_info
import datetime


def getuser(user_ID):
    this_user = Basic_info.objects.filter(idnumber=user_ID).order_by("id")
    if this_user.exists():
        for users in this_user:
            return users
    else:
        return None

def check_valid(user_ID, validdate):
    this_user = Basic_info.objects.filter(idnumber=user_ID).order_by("id")
    if not this_user.exists():
        return False
    else:
        user1 = this_user[0]
        data_array = (user1.validdate).split('-')
        start_date = datetime.datetime.strptime(data_array[0], "%Y%m%d")
        end_date = datetime.datetime.strptime(data_array[1], "%Y%m%d")
        today = datetime.datetime.today()
        if start_date <= today and end_date >= today:
            return True
        else:
            return False