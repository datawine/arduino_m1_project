from django.http import HttpResponse
from django.db import models
from django.shortcuts import render
import datetime

from collection.create import *
from collection.readinfo import *
from collection.tool import *

def checkvalid(request):
    response = ''
    request.encoding='utf-8'
    info_dict = request.GET
    print(info_dict)
    if 'validdate' in info_dict and 'idnumber' in info_dict:
        print('miaomiaomiaomiao!!!')
        flag = check_valid(int(info_dict['idnumber']), info_dict['validdate'])
        if flag:
            response = 'Good!'
        else:
            response = 'Wrong!'
    else:
        response = 'Wrong!'
    return HttpResponse("<p>" + response + "</p>")