#coding: utf-8
import serial
import time
import sys


STARTBLOCK = 5
ENDBLOCK = 14
VERSION_NUM = sys.version[0]


def clear(ser):    #初始化: 删除一些块区: 有效日期(4), 学生信息(5-6), 零钱(8), 记录(9-10,12-13)
    emptyBlock = ['\x00' for i in range(16)]
    for i in range(STARTBLOCK, ENDBLOCK+1):
        if( i % 4 != 3):           #跳过trailBlock
            write_block(ser, emptyBlock, i)

def write_block(ser, dataBlock, blockIndex):
    if(blockIndex < 10):
        blockIndex = "0"+str(blockIndex)

    #command = "w "+str(blockIndex)+" "+"".join(dataBlock)
    print(change_to_byte("w ", str(blockIndex), dataBlock))
    ser.write(change_to_byte("w ", str(blockIndex), dataBlock))
    time.sleep(1)
    line = ser.read(ser.in_waiting)
    print (line[:-1])
    print ("-------")

def read_block(ser, blockIndex):
    if(blockIndex < 10):
        blockIndex = "0"+str(blockIndex)

    command = "r "+str(blockIndex)
    ser.write(command.encode('ascii'))
    time.sleep(1)
    line = ser.read(ser.in_waiting)
    print (line[:-1])
    print ("-------")

def operate_end(ser):
    command = "close"
    print(command)
    ser.write(str.encode(command))
    time.sleep(1)
    line = ser.read(ser.in_waiting)
    print (line[:-1])
    print ("-------")

def change_to_byte(com, num, data=None):
    str_front = com + num + " "
    byte_front = str_front.encode('ascii')
    if not data == None:
        for j in data:
            ret = ord(j).to_bytes(1, 'big')
            byte_front += ret
    return byte_front

def check_basic_info(ser):
    #name, department, ID, type, sex
    print('Now we read the basic information: ')
    begin_place = 13 #读的起始位置

    command1 = "r 0"+str(5)
    ser.write(command1.encode('ascii'))
    time.sleep(1)
    line = ser.read(ser.in_waiting)[:-1].decode('ascii')
    array = line.split(' ')

    uni_name = b''
    for i in range(begin_place, begin_place+12):
        uni_name += int(array[i], 16).to_bytes(1, 'big')
        #print(int(array[i], 16))
    name = uni_name.decode('utf-8')
    print('姓名:', end=' ')
    print(name)

    sex_num = int(array[begin_place+14], 16)
    type_num = int(array[begin_place+15], 16)
    print('性别:', end=' ')
    if sex_num == 1:
        print('男')
    elif sex_num == 2:
        print('女')
    else:
        print('不详')
    print('类别:', end=' ')
    print(type_num)

    command2 = "r 0"+str(6)
    ser.write(command2.encode('ascii'))
    time.sleep(1)
    line = ser.read(ser.in_waiting)[:-1].decode('ascii')
    array = line.split(' ')

    uni_department = b''
    for i in range(begin_place, begin_place+9):
        uni_department += int(array[i], 16).to_bytes(1, 'big')
    department = uni_department.decode('utf-8')
    print('院系:', end=' ')
    print(department)

    hex_id = ''
    for i in range(begin_place+11, begin_place+16):
        hex_id += array[i]
    ID = int(hex_id, 16)
    print('学号:', end=' ')
    print(ID)

def ch2x16(s):
    clist = ''.join(s.encode("unicode_escape").decode("utf-8").split("\\u")[1: ])
    ret = int(clist, 16).to_bytes(16, 'little')
    return ret

def x162ch(b):
    ret = []
    for c in b:
        ret.append(c)
    return ret

def exactCh(chl, index):
    i = chl[index] + chl[index + 1] * 16 * 16
    c = ("\\u" + hex(i)[2:]).encode("utf-8").decode("unicode_escape")
    #print(c)
    return c

if __name__ == "__main__":
    name = input("汉字：")
    ret = ch2x16(name)
    print(ret)
    retlist = x162ch(ret)
    flag = 0
    for i in range(0, 16):
        if retlist[i] == 0:
            flag = i
            break
    flag /= 2
    ans = ''
    print(flag)
    while flag > 0:
        ans += exactCh(retlist, int(flag * 2 - 2))
        flag -= 1
    print(ans)
    #exactCh(retlist, 2)