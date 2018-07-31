import time
import sys
import requests
from tool import *

SERVER = '127.0.0.1' #主机IP  
PORT = '8000' #端口号

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
        return True
    else:
        return False
    return False