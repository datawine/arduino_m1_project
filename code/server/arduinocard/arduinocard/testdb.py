from django.http import HttpResponse
from django.db import models
from django.shortcuts import render
import datetime

from collection.create import *
from collection.readinfo import *
from collection.tool import *

def testdb(request):
    response = ' '
    #info_dict = create_from_sql(2015011245)
    #info_dict = create('小卖部一', 1, 1, '数', 2015080062, "20150901", "20190730")
    #response = str(info_dict)
    #response = ''.join(for_test(6))

    #post
    # username = request.POST['username']
    # context = {}
    # context['username'] = username
    # return render(request, '', context)

    #get
    print(request)
    request.encoding='utf-8'
    info_dict = request.GET
    if 'username' in info_dict:
        username = info_dict['username']
        response = username
    else:
        response = 'No!'
    return HttpResponse("<p>" + response + "</p>")

def testmj(request):
    response = ' '
    if check_entrance():
        response = '有效！'
    else:
        response = '假的！'
    return HttpResponse("<p>" + response + "</p>")