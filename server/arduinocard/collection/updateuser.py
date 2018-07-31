from collection.models import Basic_info
from collection.getuser import *

def create_user(info_dict):
    this_user = getuser(info_dict['idnumber'])
    if this_user == None:
        new_user = Basic_info(idnumber=info_dict['idnumber'], name=info_dict['name'], department=info_dict['department'], 
                                identifies=info_dict['identifies'], sex=info_dict['sex'], validdate=info_dict['validdate'])
        new_user.save()
        return True
    else:
        return False

def delete_user(idnumber):
    this_user = getuser(idnumber)
    if this_user == None:
        return False
    else:
        this_user.delete()
        return True