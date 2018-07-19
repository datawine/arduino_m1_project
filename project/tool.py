#coding: utf-8
import serial
import time


STARTBLOCK = 4
ENDBLOCK = 13

BLOCK5 = ['\x00' for i in range(16)]
BLOCK6 = ['\x00' for i in range(16)]

ser = serial.Serial("com3", 9600)

def create(name, sex, ty, department, ID):
#    clear()         #访问STARTBLOCK-ENDBLOCK
    
    write_name(name)    #BLOCK5
    write_sex(sex)
    write_type(ty)
#    write_department(department)  #BLOCK6
#    write_ID(ID)

    print("BLOCK5: ", BLOCK5)
#    print("BLOCK6: ", BLOCK6)

    write_block(BLOCK5, 5)
#    write_block(BLOCK6, 6)

def clear():    #初始化: 删除一些块区: 有效日期(4), 学生信息(5-6), 零钱(8), 记录(9-10,12-13)
    emptyBlock = ['\x00' for i in range(16)]
    for i in range(STARTBLOCK, ENDBLOCK+1):
        if( i % 4 != 3 ):           #跳过keyA, keyB的块区
            write_block(emptyBlock, i)



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
    BLOCK5[index] = sex
    
def write_type(ty): #类别 ty: int
    global BLOCK5
    index = 11
    BLOCK5[index] = ty
    
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

def write_block(dataBlock, blockIndex):
    if(blockIndex < 10):
        blockIndex = "0"+str(blockIndex)
    ser.write("w "+str(blockIndex)+" "+"".join(dataBlock))
    time.sleep(1)


def read_block(blockIndex):
    if(blockIndex < 10):
        blockIndex = "0"+str(blockIndex)
    ser.write("r "+str(blockIndex))
    time.sleep(1)



create("李睿燮", 1, 1, "计", 2015080062)





