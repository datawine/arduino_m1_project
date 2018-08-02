import time
import sys
import requests
import datetime
import json
import traceback
from tool import *
from create import *
from retail import *

SERVER = '127.0.0.1' #主机IP  
PORT = '8000' #端口号

#error number
SUCCESS = 1
FAILED = 0
CONSTRUCTIONERROR = 2

def check():
    b4 = read_block(ser, key, 4)
    b5 = read_block(ser, key, 5)
    b6 = read_block(ser, key, 6)

    info4 = check_info(b4, 4)
    info5 = check_info(b5, 5)
    info6 = check_info(b6, 6)
    return_dict = {**info5, **info6, **info4}
    print(return_dict)
    operate_end(ser)
    return return_dict

def check_valid():
    # idnumber = check_info(read_block(ser, key, 6), 6)['idnumber']
    # validdate = check_info(read_block(ser, key, 4), 4)['validdate']
    info_dict = {}
    while (True):
        line = ser.readline()
        print(line)
        if len(line) != 0:
            print("checking!")
            try:
                info_dict = check()
                break
            except:
                operate_end(ser)
                print("put the card again")
            else:
                pass
    url = 'http://' + SERVER + ':' + PORT + '/checkvalid'
    data = {'idnumber':str(info_dict['idnumber']), 'validdate':info_dict['validdate']}
    res=requests.get(url,params=data)
    print(res.text)
    req = res.text
    req = req[3:-4]
    if req == 'Good!':
        return SUCCESS
    else:
        return FAILED
    return FAILED

def create_new_member(name, sex, ty, department, ID, start_date, end_date):
    #需要对输入进行格式判定
    if len(name) > 6:
        return CONSTRUCTIONERROR
    if not (sex == 1 or sex == 2 or sex == 3):
        return CONSTRUCTIONERROR
    if not (ty == 1 or ty == 2 or ty == 3):
        return CONSTRUCTIONERROR
    if len(department) > 4:
        return CONSTRUCTIONERROR
    if not len(str(ID)) == 10 or not int(ID / 10000000) == 201:
        return CONSTRUCTIONERROR
    if not (check_date_valid(start_date) and check_date_valid(end_date)):
        return CONSTRUCTIONERROR
    
    url = 'http://' + SERVER + ':' + PORT + '/createcard'
    data = {'name':name, 'sex':str(sex), 'ty':str(ty), 'department':department, 'ID':str(ID), 'startdate':start_date, 'enddate':end_date}
    res=requests.get(url,params=data)
    req = res.text
    req = req[3:-4]
    print(req)
    if req == 'Success!':
        while (True):
            line = ser.readline()
            print(line)
            if len(line) != 0:
                print("Writing!")
                try:
                    create(name, sex, ty, department, ID, start_date, end_date)
                    break
                except:
                    operate_end(ser)
                    print("put the card again")
                else:
                    pass
        return SUCCESS
    else:
        return FAILED
    return FAILED

def clear_card_info():
    while (True):
        line = ser.readline()
        print(line)
        if len(line) != 0:
            print("Writing!")
            try:
                clear(ser)
                break
            except:
                operate_end(ser)
                print("put the card again")
            else:
                pass
    return SUCCESS

def clear_user_info():
    info_dict = {}
    while (True):
        line = ser.readline()
        print(line)
        if len(line) != 0:
            print("checking!")
            try:
                info_dict = check()
                break
            except:
                operate_end(ser)
                print("put the card again")
            else:
                pass
    url = 'http://' + SERVER + ':' + PORT + '/clearcard'
    data = {'idnumber':str(info_dict['idnumber'])}
    res=requests.get(url,params=data)
    req = res.text
    req = req[3:-4]
    print(req)
    if req == 'Success!':
        while (True):
            line = ser.readline()
            print(line)
            if len(line) != 0:
                print("Writing!")
                try:
                    clear(ser)
                    break
                except:
                    operate_end(ser)
                    print("put the card again")
                else:
                    pass
        return SUCCESS
    else:
        return FAILED
    return FAILED

def renew_from_sql(idnumber):
    url = 'http://' + SERVER + ':' + PORT + '/renewcard'
    data = {'idnumber':str(idnumber)}
    res=requests.get(url,params=data)
    req = res.text
    req = req[3:-4]
    print(req)
    flag_word = req[0]
    info_dict = json.loads(req[2:])
    print(info_dict)
    if flag_word == 'S':
        while (True):
            line = ser.readline()
            print(line)
            if len(line) != 0:
                print("Writing!")
                try:
                    create(info_dict['name'], int(info_dict['sex']), int(info_dict['identifies']), info_dict['department'], 
                            int(info_dict['idnumber']), info_dict['validdate'][0:8], info_dict['validdate'][9:])
                    break
                except:
                    operate_end(ser)
                    print("put the card again")
                else:
                    pass
        return SUCCESS
    else:
        return CONSTRUCTIONERROR
    return FAILED

def refresh_end_date(new_date):
    if not check_date_valid(new_date):
        return CONSTRUCTIONERROR

    info_dict = {}
    while (True):
        line = ser.readline()
        print(line)
        if len(line) != 0:
            print("checking!")
            try:
                info_dict = check()
                break
            except:
                operate_end(ser)
                print("put the card again")
            else:
                pass

    url = 'http://' + SERVER + ':' + PORT + '/refreshcard'
    data = {'idnumber':info_dict['idnumber'], 'newdate':new_date}
    res=requests.get(url,params=data)
    req = res.text
    req = req[3:-4]
    print(req)
    flag_word = req[0]
    content = req[2:10]

    if flag_word == 'S':
        start_date = content
        while (True):
            line = ser.readline()
            print(line)
            if len(line) != 0:
                print("Writing!")
                try:
                    refresh_valid(start_date, new_date)
                    break
                except:
                    operate_end(ser)
                    print("put the card again")
                else:
                    pass
        return SUCCESS
    else:
        return CONSTRUCTIONERROR
    return FAILED

def check_money():
    while (True):
        line = ser.readline()
        print(line)
        if len(line) != 0:
            print("checking!")
            try:
                query()
                break
            except:
                operate_end(ser)
                print("put the card again")
            else:
                pass
    #这个后面应该需要做成一个可以返回东西
    return False 

def regain_money_from_sql():
    info_dict = {}
    while (True):
        line = ser.readline()
        print(line)
        if len(line) != 0:
            print("checking!")
            try:
                info_dict = check()
                break
            except:
                operate_end(ser)
                print("put the card again")
            else:
                pass

    url = 'http://' + SERVER + ':' + PORT + '/regainmoney'
    data = {'idnumber':info_dict['idnumber']}
    res=requests.get(url,params=data)
    req = res.text
    req = req[3:-4]
    print(req)
    flag_word = req[0]
    content = req[2:]

    if flag_word == 'S':
        new_money = content
        print(type(new_money))
        print(new_money)
        while (True):
            line = ser.readline()
            if len(line) != 0:
                print("Writing!")
                try:
                    clear_record()
                    charge(int(new_money), "注册中心")
                    break
                except Exception as e:
                    print(str(e)+str(traceback.print_exc()))
                    operate_end(ser)
                    print("put the card again")
                else:
                    pass
        return SUCCESS
    else:
        return CONSTRUCTIONERROR
    return FAILED

def charge_in_client(number, site_name):
    info_dict = {}
    while (True):
        line = ser.readline()
        print(line)
        if len(line) != 0:
            print("checking!")
            try:
                info_dict = check()
                break
            except:
                operate_end(ser)
                print("put the card again")
            else:
                pass

    url = 'http://' + SERVER + ':' + PORT + '/chargemoney'
    data = {'idnumber':info_dict['idnumber'], 'charge':str(number)}
    res=requests.get(url,params=data)
    req = res.text
    req = req[3:-4]
    print(req)

    if req == 'Success':
        while (True):
            line = ser.readline()
            if len(line) != 0:
                print("Writing!")
                try:
                    charge(number, site_name)
                    break
                except Exception as e:
                    print(str(e))
                    operate_end(ser)
                    print("put the card again")
                else:
                    pass
        return SUCCESS
    else:
        return CONSTRUCTIONERROR
    return FAILED

def consume_in_client(number, site_name):
    info_dict = {}
    while (True):
        line = ser.readline()
        print(line)
        if len(line) != 0:
            print("checking!")
            try:
                info_dict = check()
                break
            except:
                operate_end(ser)
                print("put the card again")
            else:
                pass

    url = 'http://' + SERVER + ':' + PORT + '/consumemoney'
    data = {'idnumber':info_dict['idnumber'], 'charge':str(number)}
    res=requests.get(url,params=data)
    req = res.text
    req = req[3:-4]
    print(req)

    if req == 'Success':
        while (True):
            line = ser.readline()
            if len(line) != 0:
                print("Writing!")
                try:
                    consume(number, site_name)
                    break
                except Exception as e:
                    print(str(e))
                    operate_end(ser)
                    print("put the card again")
                else:
                    pass
        return SUCCESS
    else:
        return CONSTRUCTIONERROR
    return FAILED