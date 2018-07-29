#coding: utf-8
import serial
import time
import sys
from tool import *

import chardet

STARTBLOCK = 5
ENDBLOCK = 13
VERSION_NUM = sys.version[0]

BLOCK5 = ['\x00' for i in range(16)]
BLOCK6 = ['\x00' for i in range(16)]

# ser = serial.Serial("/dev/cu.usbmodem1421", 9600, timeout=3.0)
ser = serial.Serial("/dev/cu.usbmodem145131", 9600, timeout=3.0)


#/dev/cu.usemodem1421 (Arduino/Genuino Uno)    

def create(name, sex, ty, department, ID):
#    clear(ser)         #清空STARTBLOCK-ENDBLOCK
                   
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
    
    operate_end(ser)
    

def write_name(name): #姓名 name: string
    global BLOCK5
    index = 0
    print chardet.detect(name)
    uni_name = name.decode('utf-8')
    print(uni_name)
    for c in uni_name:
        print c
        print bytes(c)
        BLOCK5[index] = chr(c)
        index += 1
        if(index > 12):
            print('name长度大于四个字')
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
    uni_department = department.encode(encoding='utf-8')
    print(uni_department)
    for c in uni_department:
        BLOCK6[index] = chr(c)
        index += 1
        if(index > 9):
            print('department长度大于3个汉字')  
            break
        
def write_ID(ID): #学号 ID:int
    global BLOCK6
    index = 11
    ID = hex(ID)[2:]
    print('ID:')
    print(ID)
    if(len(ID) != 8):
        print('ID长度不是4字节')
        return
    for i in range(4):
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
            
            if(choice == 1):
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
    #            create("黄佩", 1, 1, "数", 2015080062)
            else:
                break


