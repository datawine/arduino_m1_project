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
    if 'validdate' in info_dict and 'idnumber' in info_dict:
        flag = check_valid(int(info_dict['idnumber']), info_dict['validdate'])
        if flag:
            response = 'Good!'
        else:
            response = 'Wrong!'
    else:
        response = 'Wrong!'
    return HttpResponse("<p>" + response + "</p>")

def createcard(request):
    response = ''
    request.encoding='utf-8'
    info_dict = request.GET
    print(info_dict)
    if 'name' in info_dict and 'sex' in info_dict and 'ty' in info_dict and 'department' in info_dict and 'ID' in info_dict and 'startdate' in info_dict and 'enddate' in info_dict:
        flag = False
        print('miaomiaomaiomao')
        new_dict = {}
        new_dict['name'] = info_dict['name']
        new_dict['sex'] = int(info_dict['sex'])
        new_dict['identifies'] = int(info_dict['ty'])
        new_dict['department'] = info_dict['department']
        new_dict['idnumber'] = int(info_dict['ID'])
        new_dict['validdate'] = info_dict['startdate'] + '-' + info_dict['enddate']
        flag = create_user(new_dict)
        if flag:
            response = 'Success!'
        else:
            response = 'Failed!'
    else:
        response = 'Failed!'
    return HttpResponse("<p>" + response + "</p>")

def cleancard(request):
    response = ''
    request.encoding='utf-8'
    info_dict = request.GET
    if 'idnumber' in info_dict:
        flag = delete_user(int(info_dict['idnumber']))
        if flag:
            response = 'Success!'
        else:
            response = 'Failed!'
    else:
        response = 'Failed!'
    return HttpResponse("<p>" + response + "</p>")