import serial
import time
import sys
from collection.tool import *
from collection.updateuser import *
from collection.getuser import *

STARTBLOCK = 5
ENDBLOCK = 13
VERSION_NUM = sys.version[0]

BLOCK4 = ['\x00' for i in range(16)]
BLOCK5 = ['\x00' for i in range(16)]
BLOCK6 = ['\x00' for i in range(16)]

#ser = serial.Serial("/dev/cu.usbmodem1421", 9600, timeout=3.0)

def check_entrance():
    idnumber = check_info(read_block(ser, key, 6), 6)['idnumber']
    validdate = check_info(read_block(ser, key, 4), 4)['validdate']
    return check_valid(idnumber, validdate)