#coding: utf-8
import serial
import time
import sys
from collection.tool import *
from collection.updateuser import *
from collection.getuser import *

import chardet

STARTBLOCK = 5
ENDBLOCK = 13
VERSION_NUM = sys.version[0]

key = "A"*16

BLOCK4 = ['\x00' for i in range(16)]
BLOCK5 = ['\x00' for i in range(16)]
BLOCK6 = ['\x00' for i in range(16)]

ser = serial.Serial("/dev/cu.usbmodem1421", 9600, timeout=3.0)
#ser = serial.Serial("/dev/cu.usbmodem145131", 9600, timeout=3.0)
  
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

    b4 = read_block(ser, key, 4)
    b5 = read_block(ser, key, 5)
    b6 = read_block(ser, key, 6)

    operate_end(ser)

    print(b4)
    print(b5)
    print(b6)

    info4 = check_info(b4, 4)
    info5 = check_info(b5, 5)
    info6 = check_info(b6, 6)
    return_dict = {**info5, **info6, **info4}
    print(return_dict)
    flag = create_user(return_dict)

    return flag

def create_from_sql(idnumber):
    this_user = getuser(idnumber)
    if this_user == None:
        return False
    else:
        write_name(this_user.name)    #BLOCK5
        write_sex(int(this_user.sex))
        write_type(int(this_user.identifies))
        write_department(this_user.department)  #BLOCK6
        write_ID(this_user.idnumber)

        write_block(ser, key, BLOCK5, 5)
        write_block(ser, key, BLOCK6, 6)

        b5 = read_block(ser, key, 5)
        b6 = read_block(ser, key, 6)
    
        operate_end(ser)

        print(check_info(b5, 5))
        print(check_info(b6, 6))

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

def init():
    global BLOCK5, BLOCK6
    BLOCK5 = ['\x00' for i in range(16)]
    BLOCK6 = ['\x00' for i in range(16)]

    
if __name__ == '__main__':
    while(True):
        print("Welcome to create card system")
        print("0.exit")
        print("1.create")
        print("2.test")
        print("3.test functions")
        if VERSION_NUM == '2':
            print('py2')
            choice = int(raw_input("Enter option: "))
            
            if(choice == 0):
                break
            elif(choice == 1):
                init()
                
                ty = int(raw_input("type: "))
                name = raw_input("name: ")
                department = raw_input("department: ")
                ID = int(raw_input("ID: "))
                sex = int(raw_input("sex(boy:1, girl:2): "))
                start_date = raw_input("valid start date: ")
                end_date = raw_input("valid end date: ")
                line = ser.readline()
                print (line[:-1])
                create(name, sex, ty, department, ID, start_date, end_date)
    #            create("黄佩", 1, 1, "数", 2015080062)
        elif VERSION_NUM == '3':
            print('py3')
            choice = int(input("Enter option: "))
            
            if choice == 1:
                init()
                ty = int(input("type: "))
                name = input("name: ")
                department = input("department: ")
                ID = int(input("ID: "))
                sex = int(input("sex(boy:1, girl:2): "))
                start_date = input("valid start date: ")
                end_date = input("valid end date: ")
                line = ser.readline()
                print (line[:-1])
                create(name, sex, ty, department, ID, start_date, end_date)
            elif choice == 2:
                create('黄佩', 1, 1, '数', 2015080062, "20150901", "20190730")
            else:
                break
