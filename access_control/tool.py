#coding: utf-8
import serial
import time
import re
from cryp import *

STARTBLOCK = 5
ENDBLOCK = 14

def clear(ser):    #初始化: 删除一些块区: 有效日期(4), 学生信息(5-6), 零钱(8), 记录(9-10,12-13)
    emptyBlock = ['\x00' for i in range(16)]
    for i in range(STARTBLOCK, ENDBLOCK+1):
        if( i % 4 != 3):           #跳过trailBlock
            write_block_raw(ser, emptyBlock, i)

def write_block_raw(ser, dataBlock, blockIndex):
    if( blockIndex % 4 == 3 ):
        print "you try to write access block"
        return
    if(blockIndex < 10):
        blockIndex = "0"+str(blockIndex)
    print(dataBlock)
    command = "w "+str(blockIndex)+" "+"".join(dataBlock)
    ser.write(command)
    time.sleep(1)
    line = ser.read(ser.in_waiting)
    print line[:-1]
    print "-------"

def read_block_raw(ser, blockIndex):
    if(blockIndex < 10):
        blockIndex = "0"+str(blockIndex)
    command = "r "+str(blockIndex)
    print(command)
    ser.write(command)
    time.sleep(1)
    line = ser.read(ser.in_waiting)
    print line[:-1]
    print "-------"
    m = re.findall(" ([\dA-F]{2})"*16, line)
    if(len(m) == 0):
        print "read_block_raw: match failed"
        return
    dataBlock = [chr(int(i,16)) for i in m[0]]
    return dataBlock 

def operate_end(ser):
    command = "close"
    print(command)
    ser.write(command)
    time.sleep(1)
    line = ser.read(ser.in_waiting)
    print line[:-1]
    print "-------"

def write_block(ser, key, dataBlock, blockIndex):
    ac = AEScrypt(key)
    en = ac.encrypt("".join(dataBlock))
    write_block_raw(ser, dataBlock, blockIndex)

def read_block(ser, key, blockIndex):
    dataBlock_raw = read_block_raw(ser, blockIndex)
    ac = AEScrypt(key)
    dataBlock = ac.decrypt("".join(dataBlock_raw))
    return dataBlock

