from django.http import HttpResponse
from django.db import models
from django.shortcuts import render
import datetime
import json

from collection.create import *
from collection.readinfo import *
from collection.tool import *
from collection.getuser import *
from collection.updateuser import *

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

def clearcard(request):
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

def renewcard(request):
    response = ''
    request.encoding='utf-8'
    info_dict = request.GET
    if 'idnumber' in info_dict:
        this_user = getuser(int(info_dict['idnumber']))
        if this_user == None:
            response = 'F'
        else:
            new_dict = {}
            new_dict['name'] = this_user.name
            new_dict['sex'] = this_user.sex
            new_dict['identifies'] = this_user.identifies
            new_dict['department'] = this_user.department
            new_dict['idnumber'] = this_user.idnumber
            new_dict['validdate'] = this_user.validdate
            string_to_send = json.dumps(new_dict)
            response = 'S ' + string_to_send
    else:
        response = 'F'
    return HttpResponse("<p>" + response + "</p>")

def refreshcard(request):
    response = ''
    request.encoding='utf-8'
    info_dict = request.GET
    if 'newdate' in info_dict and 'idnumber' in info_dict:
        flag = update_validdate(int(info_dict['idnumber']), info_dict['newdate'])
        if flag:
            this_user = getuser(int(info_dict['idnumber']))
            old_start_date = this_user.validdate
            response = 'S ' + old_start_date
        else:
            response = 'F'
    else:
        response = 'F'
    return HttpResponse("<p>" + response + "</p>")

def regainmoney(request):
    response = ''
    request.encoding='utf-8'
    info_dict = request.GET
    if 'idnumber' in info_dict:
        this_user = getuser(int(info_dict['idnumber']))
        if this_user == None:
            response = 'F'
        else:
            user_money = this_user.money
            response = 'S ' + str(user_money)
    else:
        response = 'F'
    return HttpResponse("<p>" + response + "</p>")

def chargemoney(request):
    response = ''
    request.encoding='utf-8'
    info_dict = request.GET
    if 'idnumber' in info_dict and 'charge' in info_dict:
        this_user = getuser(int(info_dict['idnumber']))
        if this_user == None:
            response = 'F'
        else:
            new_money = this_user.money + int(info_dict['charge'])
            if new_money >= 1000000:
                response = 'F'
                print('冲太多了！！！')
            else:
                this_user.money = new_money
                this_user.save()
                response = 'Success'
    else:
        response = 'F'
    return HttpResponse("<p>" + response + "</p>")

def consumemoney(request):
    response = ''
    request.encoding='utf-8'
    info_dict = request.GET
    if 'idnumber' in info_dict and 'charge' in info_dict:
        this_user = getuser(int(info_dict['idnumber']))
        if this_user == None:
            response = 'F'
        else:
            new_money = this_user.money - int(info_dict['charge'])
            if new_money < 0:
                response = 'F'
                print('没钱了！！！')
            else:
                this_user.money = new_money
                this_user.save()
                response = 'Success'
    else:
        response = 'F'
    return HttpResponse("<p>" + response + "</p>")

def getallinfo(request):
    response = ''
    return_dict = {}
    request.encoding='utf-8'
    info_dict = request.GET
    if 'clientname' in info_dict:
        user_list = getallusers()
        if len(user_list) == 0:
            response = 'F'
        else:
            for i in user_list:
                return_dict[i.idnumber] = {}
                return_dict[i.idnumber]['name'] = i.name
                return_dict[i.idnumber]['department'] = i.department
                return_dict[i.idnumber]['identifies'] = i.identifies
                return_dict[i.idnumber]['sex'] = i.sex
                return_dict[i.idnumber]['validdate'] = i.validdate
                return_dict[i.idnumber]['money'] = i.money
            string_to_send = json.dumps(return_dict)
            response = 'S ' + string_to_send
    else:
        response = 'F'
    return HttpResponse("<p>" + response + "</p>")