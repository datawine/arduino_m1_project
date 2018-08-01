import time
import sys
import requests
import datetime
from tool import *
from create import *

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
    url = 'http://' + SERVER + ':' + PORT + '/checkvalid'
    data = {'idnumber':str(info_dict['idnumber'])}
    res=requests.get(url,params=data)
    req = res.text
    req = req[3:-4]
    print(req)
    if req == 'Success!':
        while (True):
            line = ser.readline()
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

def clear_card_info():
    while (True):
        line = ser.readline()
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
    return True
    return True