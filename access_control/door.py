#coding: utf-8
import serial
import time
import sys
from tool import *

STARTBLOCK = 5
ENDBLOCK = 13
VERSION_NUM = sys.version[0]

BLOCK4 = ['\x00' for i in range(16)]
BLOCK5 = ['\x00' for i in range(16)]
BLOCK6 = ['\x00' for i in range(16)]

key = "A"*16

ser = serial.Serial("/dev/cu.usbmodem1421", 9600, timeout=3.0)
#ser = serial.Serial("/dev/cu.usbmodem145131", 9600, timeout=3.0)
  

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

            

def check_info(datablock, blocknum):
    info_dict = {}
    begin_place = 0
    array = datablock
    for i in range(0, 16):
        array[i] = hex(ord(array[i]))[2:]

    if blocknum == 5:
        uni_name = b''
        for i in range(begin_place, begin_place+12):
            uni_name += int(array[i], 16).to_bytes(1, 'big')
        print('姓名:', end=' ')
        name = decode_utf8(uni_name)
        print(name)
        info_dict['name'] = name

        sex_num = int(array[begin_place+14], 16)
        type_num = int(array[begin_place+15], 16)
        print('性别:', end=' ')
        if sex_num == 1:
            print('男')
            info_dict['sex'] = 1
        elif sex_num == 2:
            print('女')
            info_dict['sex'] = 2
        else:
            print('不详')
            info_dict['sex'] = 3
        print('类别:', end=' ')
        print(type_num)
        info_dict['identifies'] = type_num

    elif blocknum == 6:
        uni_department = b''
        for i in range(begin_place, begin_place+9):
            uni_department += int(array[i], 16).to_bytes(1, 'big')
        print('院系:', end=' ')
        department = decode_utf8(uni_department)
        print(department)
        info_dict['department'] = department

        hex_id = ''
        for i in range(begin_place+11, begin_place+16):
            hex_id += array[i]
        ID = int(hex_id, 16)
        print('学号:', end=' ')
        print(ID)
        info_dict['idnumber'] = ID
        
    elif blocknum == 4:
        d = ""
        for i in range(0, 16):
            d = d + str(int(array[begin_place + i], 16))
            if i == 7:
                d = d + "-"
        print('有效期限：', end=' ')
        print(d)
        info_dict['validdata'] = d

    return info_dict
    
if __name__ == '__main__':
    while(True):
        print("Welcome to create card system")
        print("0.exit")
        print("1.check")
        if VERSION_NUM == '2':
            print('no suppor for py2')
        elif VERSION_NUM == '3':
            print('py3')
            choice = int(input("Enter option: "))
            
            if choice == 1:
                while (True):
                    line = ser.readline()
                    if len(line) != 0:
                        print("checking!")
                        try:
                            check()
                        except:
                            operate_end(ser)
                            print("put the card again")
                        else:
                            pass
            else:
                operate_end(ser)
                break


