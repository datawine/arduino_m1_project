#coding: utf-8
import zerorpc
import serial
import time
import sys
from tool import *

STARTBLOCK = 5
ENDBLOCK = 13
VERSION_NUM = sys.version[0]

BLOCK4 = ['\x00' for i in range(16)]
BLOCK5 = ['\x00' for i in range(16)]
BLOCK6 = ['\x00' for i in range(16)]

key = "A"*16
'''
#ser = serial.Serial("/dev/cu.usbmodem1421", 9600, timeout=3.0)
ser = serial.Serial("/dev/cu.usbmodem145131", 9600, timeout=3.0)
#ser = serial.Serial("/dev/ttyS0", 9600, timeout=3.0)
'''
class CreateSystem(object):
    def create_card(self, name, sex, ty, department, ID, start_date, end_date):
#        global create, read_block
        try:
            #info = create(name, int(sex), int(ty), department, int(ID), start_date, end_date)
            info = "name: "+name+"sex: "+sex+"ty: "+ty+"department: "+department+"ID: "+ID+"start_date: "+start_date+"end_date: "+end_date
            with open("./test.txt", "w") as f:
                f.write(info)
            print(info)
            return info
        except Exception as e:
            return str(e)
    def echo(self, text):
        return text

def create(name, sex, ty, department, ID, start_date, end_date):
    try:
        clear(ser)         #清空STARTBLOCK-ENDBLOCK

        write_name(name)    #BLOCK5
        write_sex(sex)
        write_type(ty)
        write_department(department)  #BLOCK6
        write_ID(ID)
        write_valid(start_date, end_date)

        print("BLOCK4: ", BLOCK4)    
        print("BLOCK5: ", BLOCK5)
        print("BLOCK6: ", BLOCK6)

        write_block(ser, key, BLOCK4, 4)
        write_block(ser, key, BLOCK5, 5)
        write_block(ser, key, BLOCK6, 6)
        
        b4 = read_block(ser, key, 4)
        b5 = read_block(ser, key, 5)
        b6 = read_block(ser, key, 6)
        
        
        info4 = check_info(b4, 4)
        info5 = check_info(b5, 5)
        info6 = check_info(b6, 6)
        return_dict = {**info5, **info6, **info4}
        print(return_dict)
        operate_end(ser)
          
        return str(return_dict)
        
    except Exception as e:
        return str(e)+str(traceback.print_exc())
    
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
    global BLOCK4, BLOCK5, BLOCK6
    BLOCK4 = ['\x00' for i in range(16)]
    BLOCK5 = ['\x00' for i in range(16)]
    BLOCK6 = ['\x00' for i in range(16)]

def parse_port():
    port = 4242
    try:
        port = int(sys.argv[1])
    except Exception as e:
        pass
    return '{}'.format(port)

def main():
    addr = 'tcp://127.0.0.1:' + parse_port()
    s = zerorpc.Server(CreateSystem())
    s.bind(addr)
    print('start running on {}'.format(addr))
    s.run()

if __name__ == '__main__':
    main()

