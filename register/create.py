#coding: utf-8
import serial
import time
from tool import *

STARTBLOCK = 5
ENDBLOCK = 13

BLOCK5 = ['\x00' for i in range(16)]
BLOCK6 = ['\x00' for i in range(16)]

ser = serial.Serial("com3", 9600)


    

def create(name, sex, ty, department, ID):
    clear(ser)         #清空STARTBLOCK-ENDBLOCK
                   
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
    for c in name:
        BLOCK5[index] = c
        index += 1
        if(index > 10):
            print('name长度大于10字节')
            break
        
def write_sex(sex): #性别 sex: int
    global BLOCK5
    index = 10
    BLOCK5[index] = chr(sex)
    
def write_type(ty): #类别 ty: int
    global BLOCK5
    index = 11
    BLOCK5[index] = chr(ty)
    
def write_department(department): #院系  department: string
    global BLOCK6
    index = 0
    for c in department:
        BLOCK6[index] = c
        index += 1
        if(index > 8):
            print('department长度大于8字节')  
            break
        
def write_ID(ID): #学号 ID:int
    global BLOCK6
    index = 8
    ID = hex(ID)[2:]
    if(len(ID) != 8):
        print('ID长度不是4字节')
        return
    for i in range(4):
        BLOCK6[index] = chr(int(ID[i:i+2],16))
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
            print line[:-1]
            create(name, sex, ty, department, ID)
#            create("黄佩", 1, 1, "数", 2015080062)
            


