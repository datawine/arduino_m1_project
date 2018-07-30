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

BLOCK5 = ['\x00' for i in range(16)]
BLOCK6 = ['\x00' for i in range(16)]

ser = serial.Serial("/dev/cu.usbmodem1421", 9600, timeout=3.0)
#ser = serial.Serial("/dev/cu.usbmodem145131", 9600, timeout=3.0)
  

def create(name, sex, ty, department, ID):
    #clear(ser)         #清空STARTBLOCK-ENDBLOCK
                   
    write_name(name)    #BLOCK5
    write_sex(sex)
    write_type(ty)
    write_department(department)  #BLOCK6
    write_ID(ID)

    print("BLOCK5: ", BLOCK5)
    print("BLOCK6: ", BLOCK6)

    write_block(ser, BLOCK5, 5)
    write_block(ser, BLOCK6, 6)

    read_block(ser, 5)
    read_block(ser, 6)

    return_dict = check_basic_info(ser)
    flag = create_user(return_dict)
    
    operate_end(ser)
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

        write_block(ser, BLOCK5, 5)
        write_block(ser, BLOCK6, 6)

        read_block(ser, 5)
        read_block(ser, 6)

        print(check_basic_info(ser))
    
        operate_end(ser)

        return True

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

    
if __name__ == '__main__':
    while(True):
        print("Welcome to create card system")
        print("0.exit")
        print("1.create")
        print("2.test")
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
                print("please put your card")
                line = ser.readline()
                print (line[:-1])
                create(name, sex, ty, department, ID)
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
                print("please put your card")
                line = ser.readline()
                print (line[:-1])
                create(name, sex, ty, department, ID)
            elif choice == 2:
                create('黄佩', 1, 1, '数', 2015080062)
            else:
                break
