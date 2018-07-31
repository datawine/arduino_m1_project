#coding: utf-8
import serial
import time
import sys
from datetime import *
from tool import *

STARTBLOCK = 5
ENDBLOCK = 13
VERSION_NUM = sys.version[0]

BLOCK8 = ['\x00' for i in range(16)]

key = "A"*16

#ser = serial.Serial("/dev/cu.usbmodem1421", 9600, timeout=3.0)
ser = serial.Serial("/dev/cu.usbmodem145141", 9600, timeout=3.0)

def query():
    s, n = read_money_info()
    print("卡内余额:", end = ' ')
    print(s)

    print("共{}条消费记录:".format(n))
    parse_record(n)
    for i in range(n):
        if record[i][2] == 0:
            print("在 {} 于 {} 充值 {} 元"\
                .format(record[i][1], record[i][2], record[i][0]), end = ' ')
        elif record[i][2] == 1:
            print("在 {} 于 {} 消费 {} 元"\
                .format(record[i][1], record[i][2], record[i][0]), end = ' ')

def charge(s, site_name):
    tmps, tmpn = read_money_info()
    if tmps + s >= 10000.0:
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
        tmptime = str(datetime.new().month).zfill(2) + "/" + \
                str(datetime.new().day).zfill(2) + "/" + \
                str(datetime.new().hour).zfill(2) + ":" + \
                str(datetime.new().minute).zfill(2)
        record.append([s, t, site_name, 0])
        write_num(n)

        write_block_raw(ser, BLOCK8, 8)
        write_record(record)

def consume(s, site_name):
    tmps, tmpn = read_money_info()
    if tmps - s >= 0.0:
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
        tmptime = str(datetime.new().month).zfill(2) + "/" + \
                str(datetime.new().day).zfill(2) + "/" + \
                str(datetime.new().hour).zfill(2) + ":" + \
                str(datetime.new().minute).zfill(2)
        record.append([s, t, site_name, 1])
        write_num(n)

        write_block_raw(ser, BLOCK8, 8)
        write_record(record)

def read_money_info():
    line = read_block_raw(ser, 8)
    array = line.split(' ')
    return parse_money_sum(array), parse_record_num(array)

def parse_money_sum(array):
    s = 0
    s = s + int(array[begin_place + 2], 16) * (10 ** -2)
    s = s + int(array[begin_place + 1], 16) * (10 ** 0)
    s = s + int(array[begin_place + 0], 16) * (10 ** 2)
    return s

def parse_record_num(array):
    return int(array[begin_place + 15], 16)

def parse_record(num):
    global record
    record = []
    r_index = [9, 10, 12, 13, 14]
    cnt = 0
    while cnt < num:
        line = read_block_raw(ser, r_index[cnt])
        array = line.split(' ')
        s = parse_money_sum(array)
        ty = int(array[begin_place + 15], 16)
        uni_name = b''
        for i in range(begin_place + 7, begin_place + 15):
            uni_name += int(array[i], 16).to_bytes(1, 'big')        
        uni_name = decode_utf8(uni_name)
        t = ""
        t_month = str(int(array[begin_place + 3], 16)).zfill(2)
        t_day = str(int(array[begin_place + 4], 16)).zfill(2)
        t_hour = str(int(array[begin_place + 5], 16).zfill(2)
        t_min = str(int(array[begin_place + 6], 16).zfill(2)
        t = t_month + "/" + t_day + "/" + t_hour + ":" + t_min

        record.append([s, t, uni_name, ty])
        cnt = cnt + 1
    return record

def write_record(record_list):
    r_index = [9, 10, 12, 13, 14]
    cnt = 0
    for rec in record_list:
        tmpblock = ['\x00' for i in range(16)]
        write_money(record[0], tmpblock)
        write_time(record[1], tmpblock)
        write_site(record[2], tmpblock)
        write_type(record[3], tmpblock)
        write_block_raw(ser, tmpblock, r_index[cnt])
        cnt = cnt + 1

def write_money(s, tmpblock):
    index = 0
    tmpblock[index] = chr(int(s // 10000) % 10)
    tmpblock[index + 1] = chr(int(s // 100) % 10)
    tmpblock[index + 2] = chr(int(s * 100) % 100)

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
    tmpblock[index] = chr(t[0:2])
    tmpblock[index + 1] = chr(t[3:5])
    tmpblock[index + 2] = chr(t[6:8])
    tmpblock[index + 3] = chr(t[9:])

def write_type(ty, tmpblock):
    index = 15
    tmpblock[index] = chr(ty)

def init():
    global BLOCK8
    BLOCK8 = ['\x00' for i in range(16)]

site_name = "小卖部1"

if __name__ == '__main__':
    while(True):
        print("Welcome to retailing system")
        print("0.exit")
        print("1.query")
        print("2.charge")
        print("3.consume")
        if VERSION_NUM == '2':
            print('py2')
            print("no python2 sypport yet")
        elif VERSION_NUM == '3':
            print('py3')
            choice = int(input("Enter option: "))
            
            if choice == 1:
                line = ser.readline()
                print (line[:-1])
                create(name, sex, ty, department, ID, start_date, end_date)
            elif choice == 2:
                line = ser.readline()
                print (line[:-1])
                create('黄佩', 1, 1, '数', 2015080062, "20150901", "20190730")
            else:
                break


