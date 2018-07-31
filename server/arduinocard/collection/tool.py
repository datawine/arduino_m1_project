#coding: utf-8
import serial
import time
import sys
from collection.cryp import *
import re

STARTBLOCK = 5
ENDBLOCK = 14
VERSION_NUM = sys.version[0]
key = "A"*16

ser = serial.Serial("/dev/cu.usbmodem1421", 9600, timeout=3.0)
#ser = serial.Serial("/dev/cu.usbmodem145131", 9600, timeout=3.0)

def clear(ser):    #初始化: 删除一些块区: 有效日期(4), 学生信息(5-6), 零钱(8), 记录(9-10,12-13)
    emptyBlock = ['\x00' for i in range(16)]
    for i in range(STARTBLOCK, ENDBLOCK+1):
        if( i % 4 != 3):           #跳过trailBlock
            write_block(ser, key, emptyBlock, i)

def write_block_raw(ser, dataBlock, blockIndex):
    if( blockIndex % 4 == 3 ):
        print("you try to write on trailer block")
        return
    if(blockIndex < 10):
        blockIndex = "0"+str(blockIndex)
    ser.write(change_to_byte("w ", str(blockIndex), dataBlock))
    time.sleep(1)
    line = ser.read(ser.in_waiting)
    print (line[:-1])
    print ("-------")

def read_block_raw(ser, blockIndex):
    if(blockIndex < 10):
        blockIndex = "0"+str(blockIndex)

    command = "r "+str(blockIndex)
    ser.write(command.encode('ascii'))
    time.sleep(1)
    line = ser.read(ser.in_waiting)[:-1].decode('ascii')
    m = re.findall(" ([\dA-F]{2})"*16, line)
    if(len(m) == 0):
        print ("read_block_raw: match failed")
        return
    dataBlock = [chr(int(i,16)) for i in m[0]]
    return dataBlock 

def write_block(ser, key, dataBlock, blockIndex):
    ac = AEScrypt(key)
    en = ac.encrypt("".join(dataBlock))
    write_block_raw(ser, en, blockIndex)

def read_block(ser, key, blockIndex):
    dataBlock_raw = read_block_raw(ser, blockIndex)
    ac = AEScrypt(key)
    dataBlock = [i for i in ac.decrypt("".join(dataBlock_raw))]
    return dataBlock

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

def encode_utf8(s):
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

def decode_utf8(ret):
    retlist = x162ch(ret)
    flag = 0
    i = 0
    while(i < 12):
        if retlist[i] == 0 and retlist[i+1] == 0:
            flag = i
            break
        i += 2
    flag /= 2
    ans = ''
    while flag > 0:
        ans += exactCh(retlist, int(flag * 2 - 2))
        flag -= 1
    return ans

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
        info_dict['validdate'] = d

    return info_dict

if __name__ == "__main__":
    name = input("汉字：")
    ret = encode_utf8(name)
    print(ret)
    
    print(decode_utf8(ret))
    #exactCh(retlist, 2)