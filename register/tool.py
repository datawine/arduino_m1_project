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
    print(dataBlock)
    command = "w "+str(blockIndex)+" "+"".join(dataBlock)
    ser.write(str.encode(command))
    time.sleep(1)
    line = ser.read(ser.in_waiting)
    print (line[:-1])
    print ("-------")

def read_block(ser, blockIndex):
    if(blockIndex < 10):
        blockIndex = "0"+str(blockIndex)
    command = "r "+str(blockIndex)
    print(command)
    ser.write(str.encode(command))
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
    print(c)

if __name__ == "__main__":
    name = input("汉字：")
    ret = ch2x16(name)
    retlist = x162ch(ret)
    exactCh(retlist, 0)