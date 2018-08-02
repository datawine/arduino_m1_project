#coding: utf-8
import serial
import time
import sys
from datetime import *
import datetime
from tool import *

STARTBLOCK = 5
ENDBLOCK = 13
VERSION_NUM = sys.version[0]

BLOCK8 = ['\x00' for i in range(16)]

key = "A"*16

ser = serial.Serial("/dev/cu.usbmodem1421", 9600, timeout=3.0)
#ser = serial.Serial("/dev/cu.usbmodem145131", 9600, timeout=3.0)

def query():
    s, n = read_money_info()
    print("卡内余额:", end = ' ')
    print(s * 0.01)

    print("共{}条消费记录:".format(n))
    parse_record(n)
    for i in range(n):
        if record[i][3] == 0:
            print("在 {} 于 {} 充值 {} 元"\
                .format(record[i][1], record[i][2], record[i][0] * 0.01), end = ' ')
            print()
        elif record[i][3] == 1:
            print("在 {} 于 {} 消费 {} 元"\
                .format(record[i][1], record[i][2], record[i][0] * 0.01), end = ' ')
            print()

    operate_end(ser)

def query_money():
    s, n = read_money_info()
    operate_end(ser)
    money_len = len(str(s))
    money_int = str(s)[0:-2]
    money_flo = str(s)[(money_len-2):]
    return_str = money_int + '.' + money_flo
    return str(return_str)

def query_record_time():
    s, n = read_money_info()
    parse_record(n)
    return_str = ''
    for i in range(n):
        if record[i][3] == 0:
            orders = 'chuisimaoyu'
        elif record[i][3] == 1:
            this_str = str(record[i][1]) + "|"
            return_str += this_str

    operate_end(ser)
    return return_str

def query_record_num():
    s, n = read_money_info()
    parse_record(n)
    return_str = ''
    for i in range(n):
        if record[i][3] == 0:
            orders = 'mobaomaoyu'
        elif record[i][3] == 1:
            money_len = len(str(record[i][0]))
            money_int = str(record[i][0])[0:-2]
            money_flo = str(record[i][0])[(money_len-2):]
            this_str = money_int + '.' + money_flo + "|"
            return_str += this_str

    operate_end(ser)
    return return_str

def charge(s, site_name):
    tmps, tmpn = read_money_info()
    if tmps + s >= 1000000:
        print("充值失败：账户中不能超过9999.99元", end = ' ')
    else:
        init()
        tmpblock = ['\x00' for i in range(16)]
        write_money(tmps + s, BLOCK8)
        if tmpn < 5:
            n = tmpn + 1
            record = parse_record(tmpn)
        else:
            n = tmpn
            record = parse_record(tmpn)[1:]
        tmptime = str(datetime.datetime.now().month).zfill(2) + "/" + \
                str(datetime.datetime.now().day).zfill(2) + "/" + \
                str(datetime.datetime.now().hour).zfill(2) + ":" + \
                str(datetime.datetime.now().minute).zfill(2)
        record.append([s, tmptime, site_name, 0])
        write_num(n)

        write_block(ser, key, BLOCK8, 8)
        write_record(record)

        operate_end(ser)

def consume(s, site_name):
    tmps, tmpn = read_money_info()
    if tmps - s < 0:
        print("消费失败：账户余额不足，请充值", end = ' ')
    else:
        init()
        tmpblock = ['\x00' for i in range(16)]
        write_money(tmps - s, BLOCK8)
        if tmpn < 5:
            n = tmpn + 1
            record = parse_record(tmpn)
        else:
            n = tmpn
            record = parse_record(tmpn)[1:]
        tmptime = str(datetime.datetime.now().month).zfill(2) + "/" + \
                str(datetime.datetime.now().day).zfill(2) + "/" + \
                str(datetime.datetime.now().hour).zfill(2) + ":" + \
                str(datetime.datetime.now().minute).zfill(2)
        record.append([s, tmptime, site_name, 1])
        write_num(n)

        write_block(ser, key, BLOCK8, 8)
        write_record(record)

        operate_end(ser)

def read_money_info():
    array = read_block(ser, key, 8)
    for i in range(0, 16):
        array[i] = hex(ord(array[i]))[2:]
    return parse_money_sum(array), parse_record_num(array)

def parse_money_sum(array):
    s = 0
    s = s + int(array[2], 16) * (10 ** 0)
    s = s + int(array[1], 16) * (10 ** 2)
    s = s + int(array[0], 16) * (10 ** 4)
    return s

def parse_record_num(array):
    return int(array[15], 16)

def parse_record(num):
    global record
    record = []
    r_index = [9, 10, 12, 13, 14]
    cnt = 0
    while cnt < num:
        array = read_block(ser, key, r_index[cnt])
        for i in range(0, 16):
            array[i] = hex(ord(array[i]))[2:]
        s = parse_money_sum(array)
        ty = int(array[15], 16)
        uni_name = b''
        for i in range(7, 15):
            uni_name += int(array[i], 16).to_bytes(1, 'big')       
        uni_name = decode_utf8(uni_name)
        t = ""
        t_month = str(int(array[3], 16)).zfill(2)
        t_day = str(int(array[4], 16)).zfill(2)
        t_hour = str(int(array[5], 16)).zfill(2)
        t_min = str(int(array[6], 16)).zfill(2)
        t = t_month + "/" + t_day + "/" + t_hour + ":" + t_min

        record.append([s, t, uni_name, ty])
        cnt = cnt + 1
    return record

def write_record(record_list):
    r_index = [9, 10, 12, 13, 14]
    cnt = 0
    for rec in record_list:
        tmpblock = ['\x00' for i in range(16)]
        write_money(rec[0], tmpblock)
        write_time(rec[1], tmpblock)
        write_site(rec[2], tmpblock)
        write_type(rec[3], tmpblock)
        write_block(ser, key, tmpblock, r_index[cnt])
        cnt = cnt + 1

def write_money(s, tmpblock):
    index = 0
    tmpblock[index] = chr(int(s // 10000) % 100)
    tmpblock[index + 1] = chr(int(s // 100) % 100)
    tmpblock[index + 2] = chr(int(s // 1) % 100)

def write_num(num):
    global BLOCK8
    index = 15
    BLOCK8[index] = chr(num)

def write_site(site_name, tmpblock):
    index = 7
    name_len = len(site_name)
    len_num = 0
    uni_name = encode_utf8(site_name)
    for c in uni_name:
        if index > 14:
            print('站点名称长度大于4个字')
            break
        tmpblock[index] = chr(c)
        index += 1
        len_num += 1
        if len_num > name_len * 2 - 1:
            break

def write_time(t, tmpblock):
    index = 3
    tmpblock[index] = chr(int(t[0:2]))
    tmpblock[index + 1] = chr(int(t[3:5]))
    tmpblock[index + 2] = chr(int(t[6:8]))
    tmpblock[index + 3] = chr(int(t[9:]))

def write_type(ty, tmpblock):
    index = 15
    tmpblock[index] = chr(ty)

def write_in_money(num):
    write_num(num)
    write_block(ser, key, BLOCK8, 8)

def clear_record():
    emptyBlock = ['\x00' for i in range(16)]
    for i in range(8, 15):
        if( i % 4 != 3):           #跳过trailBlock
            write_block(ser, key, emptyBlock, i)

def init():
    global BLOCK8
    BLOCK8 = ['\x00' for i in range(16)]

site_name = "小卖部"

if __name__ == '__main__':
    print("Welcome to retailing system")
    line = ser.readline()
    print (line[:-1])
    while(True):
        print("---------------")
        print("0.exit")
        print("1.query")
        print("2.charge")
        print("3.consume")
        if VERSION_NUM == '2':
            print('py2')
            print("no python2 sypport yet")
        elif VERSION_NUM == '3':
            choice = int(input("Enter option: "))
            
            if choice == 1:
                query()
            elif choice == 2:
                s = int(float(input("Enter money to charge:")) * 100 // 1)
                charge(s, site_name)
            elif choice == 3:
                s = int(float(input("Enter money to consume:")) * 100 // 1)
                consume(s, site_name)
            else:
                operate_end(ser)
                break

