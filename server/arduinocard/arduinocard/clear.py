from django.http import HttpResponse
from django.db import models
import datetime
from collection.updateuser import *

def clear(request):
    response = ' '
    response = str(delete_user(2015080062))
    return HttpResponse("<p>" + response + "</p>")