import time
import sys
import requests
import datetime
import json
import traceback
import zerorpc
from tool import *
from create import *
from retail import *

SERVER = '127.0.0.1' #主机IP  
PORT = '8000' #端口号

#error number
SUCCESS = 1
FAILED = 0
CONSTRUCTIONERROR = 2

class CreateSystem(object):
    def create_card(self, name, sex, ty, department, ID, start_date, end_date):
#        global create, read_block
        try:
            #info = create(name, int(sex), int(ty), department, int(ID), start_date, end_date)
            info = "name: "+name+"sex: "+sex+"ty: "+ty+"department: "+department+"ID: "+ID+"start_date: "+start_date+"end_date: "+end_date
            with open("./test.txt", "w") as f:
                f.write(info)
            print(info)
            return info
        except Exception as e:
            return str(e)
    def create_new(self, name, sex, ty, department, ID, start_date, end_date):
        if len(department) > 4:
            department = department[0:4]
        if len(name) > 6:
            name = name[0:6]
        start_date = start_date[0:4] + start_date[5:7] + start_date[8:10]
        end_date = end_date[0:4] + end_date[5:7] + end_date[8:10]
        flag = False
        try:
            flag = create_new_member(name, int(sex), int(ty), department, int(ID), start_date, end_date) 
        except:
            return '创建失败！发生错误！！'
        else:
            pass
        if flag == SUCCESS:
            return '创建成功！'
        elif flag == FAILED:
            return '创建失败！信息错误！！'
        elif flag == CONSTRUCTIONERROR:
            return '创建失败！格式错误！！'

    def refresh_card(self, new_end_date):
        new_end_date = new_end_date[0:4] + new_end_date[5:7] + new_end_date[8:10]
        flag = False
        try:
            flag = refresh_end_date(new_end_date)
        except:
            return '注册失败！发生错误！！'
        else:
            pass
        if flag == SUCCESS:
            return '注册成功！'
        elif flag == FAILED:
            return '注册失败！'
        elif flag == CONSTRUCTIONERROR:
            return '注册失败！信息错误！！'
        return True

    def clear_cards(self, signal1, signal2):
        return signal1+' '+signal2

    def echo(self, text):
        return text

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
    with open('./valid.json', 'r') as v:
        valid_dict = json.load(v)

    info_dict = {}
    while (True):
        line = ser.readline()
        print(line)
        if len(line) != 0:
            print("checking!")
            try:
                info_dict = check()
                break
            except Exception as e:
                print(str(e)+str(traceback.print_exc()))
                operate_end(ser)
                print("put the card again")
            else:
                pass

    if not str(info_dict['idnumber']) in valid_dict:
        print('miao')
        return CONSTRUCTIONERROR
    else:
        if not valid_dict[str(info_dict['idnumber'])]:
            return FAILED
    print('???')
    try:
        url = 'http://' + SERVER + ':' + PORT + '/checkvalid'
        data = {'idnumber':str(info_dict['idnumber']), 'validdate':info_dict['validdate']}
        res=requests.get(url,params=data)
        print(res.text)
        req = res.text
        req = req[3:-4]
        print('联网门禁！')
        if req == 'Good!':
            return SUCCESS
        else:
            return FAILED
    except:
        print('断网门禁！')
        with open('./data.json', 'r') as f:
            data = json.load(f)
            idnumber = str(info_dict['idnumber'])
            if idnumber in data:
                validdate = data[idnumber]['validdate']
                start_date = datetime.datetime.strptime(validdate[0:8], "%Y%m%d")
                end_date = datetime.datetime.strptime(validdate[9:17], "%Y%m%d")
                today = datetime.datetime.today()
                if start_date <= today and end_date >= today:
                    return SUCCESS
                else:
                    return FAILED
            else:
                return CONSTRUCTIONERROR
    else:
        return FAILED

def create_new_member(name, sex, ty, department, ID, start_date, end_date):
    #需要对输入进行格式判定
    print(name, sex, ty, department, ID, start_date, end_date)
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

def get_info_from_sql(site_name):
    url = 'http://' + SERVER + ':' + PORT + '/getallinfo'
    data = {'clientname':site_name}
    res=requests.get(url,params=data)
    req = res.text
    req = req[3:-4]
    flag_word = req[0]
    info_dict = json.loads(req[2:])
    print(info_dict)
    valid_dict = {}
    for i in info_dict:
        valid_dict[i] = False
    if flag_word == 'S':
        with open('./data.json', 'w') as f:
            json.dump(info_dict, f)
        with open('./valid.json', 'w') as v:
            json.dump(valid_dict, v)
        return True
    return False

def add_valid_user(id_list):
    valid_dict = {}
    with open('./valid.json', 'r') as v1:
        valid_dict = json.load(v1)
    with open('./data.json', 'r') as f:
        data = json.load(f)

    for ids in id_list:
        if ids in data:
            valid_dict[ids] = True
        else:
            return CONSTRUCTIONERROR

    with open('./valid.json', 'w') as v2:
        json.dump(valid_dict, v2)

    return SUCCESS

def parse_port():
    port = 4242
    try:
        port = int(sys.argv[1])
    except Exception as e:
        pass
    return '{}'.format(port)

def main():
    addr = 'tcp://127.0.0.1:' + parse_port()
    s = zerorpc.Server(CreateSystem())
    s.bind(addr)
    print('start running on {}'.format(addr))
    s.run()

if __name__ == '__main__':
    main()