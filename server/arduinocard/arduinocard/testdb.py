from django.http import HttpResponse
from django.db import models
import datetime

from collection.create import *
from collection.tool import *

ser = serial.Serial("/dev/cu.usbmodem1421", 9600, timeout=3.0)

def testdb(request):
    response = ' '
    info_dict = create('黄佩', 1, 1, '数', 2015080062)
    #info_dict = check_basic_info(ser)
    response = str(info_dict)
    return HttpResponse("<p>" + response + "</p>")