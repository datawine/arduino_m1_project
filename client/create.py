#coding: utf-8
import serial
import time
import sys
from tool import *

BLOCK4 = ['\x00' for i in range(16)]
BLOCK5 = ['\x00' for i in range(16)]
BLOCK6 = ['\x00' for i in range(16)]

def for_test(num):
    return read_block(ser, key, num)

def create(name, sex, ty, department, ID, start_date, end_date):
    clear(ser)         #清空STARTBLOCK-ENDBLOCK
                   
    write_name(name)    #BLOCK5
    write_sex(sex)
    write_type(ty)
    write_department(department)  #BLOCK6
    write_ID(ID)
    write_valid(start_date, end_date) # BLOCK4

    print("BLOCK4: ", BLOCK4)    
    print("BLOCK5: ", BLOCK5)
    print("BLOCK6: ", BLOCK6)

    write_block(ser, key, BLOCK4, 4)
    write_block(ser, key, BLOCK5, 5)
    write_block(ser, key, BLOCK6, 6)

    operate_end(ser)

    return True

def write_valid(start_date, end_date):
    global BLOCK4
    d = start_date + end_date
    if len(d) != 16:
        print("错误日期格式，日期格式应如20180726")
    for i in range(0, len(d)):
        BLOCK4[i] = chr(int(d[i]))

def write_name(name): #姓名 name: string
    global BLOCK5
    index = 0
    name_len = len(name)
    len_num = 0
    uni_name = encode_utf8(name)
    for c in uni_name:
        BLOCK5[index] = chr(c)
        index += 1
        len_num += 1
        if len_num > name_len * 2 - 1:
            break
        if index > 12:
            print('name长度大于6个字')
            break
        
def write_sex(sex): #性别 sex: int
    global BLOCK5
    index = 14
    BLOCK5[index] = chr(sex)
    
def write_type(ty): #类别 ty: int
    global BLOCK5
    index = 15
    BLOCK5[index] = chr(ty)
    
def write_department(department): #院系  department: string
    global BLOCK6
    index = 0
    department_len = len(department)
    len_num = 0
    uni_department = encode_utf8(department)
    for c in uni_department:
        BLOCK6[index] = chr(c)
        index += 1
        len_num += 1
        if len_num > department_len * 2 - 1:
            break
        if index > 8:
            print('department长度大于4个汉字')  
            break
        
def write_ID(ID): #学号 ID:int
    global BLOCK6
    index = 11
    ID = hex(ID)[2:]
    while len(ID) < 10:
        ID = '0' + ID
    print('ID:')
    print(ID)

    if(len(ID) != 10):
        print('ID长度不是5字节')
    for i in range(5):
        BLOCK6[index] = chr(int(ID[i*2:i*2+2],16))
        index += 1

def init():
    global BLOCK5, BLOCK6
    BLOCK5 = ['\x00' for i in range(16)]
    BLOCK6 = ['\x00' for i in range(16)]