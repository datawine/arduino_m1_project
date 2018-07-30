from django.http import HttpResponse
from django.db import models
import datetime

from collection.create import *
from collection.tool import *

def testdb(request):
    response = ' '
    #info_dict = create('黄佩', 1, 1, '数', 2015080062)
    info_dict = create_from_sql(2015011245)
    response = str(info_dict)
    return HttpResponse("<p>" + response + "</p>")